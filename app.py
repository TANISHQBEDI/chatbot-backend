from huggingface_hub import InferenceClient
import re
import os
from sqlalchemy import create_engine, text
# from sqlalchemy import text


HF_API_KEY = os.environ.get("HF_API_KEY")
HF_MODEL_NAME = os.environ.get("HF_MODEL_NAME")

db_path = 'test.db'
# db_path = 'crewAIdb.db' 
engine = create_engine(f'sqlite:///{db_path}')
db = engine

from gradio_client import Client

sql_client = Client("garvit2205/SQL_query_generator")



class CricketWebBot:
    def __init__(self):
        """
        Initialize the cricket chatbot with web scraping capabilities
        """
        
        self.player_id_cache = {}

        self.client = InferenceClient(api_key=HF_API_KEY)

    def sql_query_for_team_ranking(self, query: str, temperature: float = 0.7, top_p: float = 0.9, max_tokens: int = 520):
        """
        This agent generates SQL queries for the rankings of teams based on the given query.
        
        Table name: men_team_rankings
        Table format:
            | Ranking | Country | Weighted Matches | Points | Rating | Format | Gender |
        
        
        
        Args:
            query (str): User's query about team rankings.
            db (object): Database connection object for validation (optional, if needed).
            temperature (float): Sampling temperature for LLM response generation.
            top_p (float): Nucleus sampling parameter for LLM.
            max_tokens (int): Maximum number of tokens in the LLM's response.
        
        Returns:
            str: Generated SQL query or an appropriate error message.
        """
        try:
            # Define the system message for query generation

            prompt=f'''
                You are a helpful assistant who generates SQL queries.\n
                The queries should retrieve information from the 'men_team_rankings' table, which has the following structure:\n
                | Ranking | Country | Weighted Matches | Points | Rating | Format | Gender |\n
                
                Write efficient SQL queries based on the user's request, ensuring proper formatting and syntax.\n
                Format can be of the three : 'Test', 'ODI' or 'T20I'\n
                Gender can be : 'Men' or 'Women'\n
                While searching ignore case\n
                Keep in mind to use LIKE for entity names\n
                If 'Gender' not given use 'Men' as default\n
                If 'Format' not given use 'ODI' as default\n
                Unless specified give the result based on the 'Ranking' Column\n
                Just give the sql query as output\n
                User Query : {query}
            '''

            result = sql_client.predict(
                    user_query=prompt,
                    api_name="/predict"
            )
            print('space result : ')
            print(result)
            
            # Optional: Validate the SQL query using the provided database connection
            # print(db)
            if db:
                print('inside db')
                try:
                    print('inside try')
                    with db.connect() as connection:
                        result = connection.execute(text(result))  # Executes the SQL query
                        explanation = result.fetchall()  # Fetch the results of EXPLAIN
                        explanation = "\n".join(
                            [f"Ranking : {row[0]}, Country: {row[1]}, Weighted Matches: {row[2]}, Points: {row[3]}, Rating: {row[4]}, Format: {row[5]}, Gender: {row[6]} |"
                            for row in explanation]
                        )
                        print(f'sql answer : \n{explanation}')
                    
                    messages=[
                        {
                            "role": "system",
                            "content": (
                               "The below is some data regarding cricket team rankings.\n"
                               "The format of the data is as : | Ranking | Country | Weighted Matches | Points | Rating | Format | Gender |\n"
                               f"Based on the query : {query} ; give answer"
                            ),
                        },
                        {"role": "user", "content": explanation},
                    ]

                    response = self.client.chat.completions.create(
                        model="meta-llama/Llama-3.2-3B-Instruct",
                        messages=messages,
                        max_tokens=max_tokens,
                        temperature=temperature,
                        top_p=top_p,
                    )

                    # print(response)

                    # Extract the response content
                    result = response["choices"][0]["message"].get("content", "No content returned.")
                except Exception as validation_error:
                    print(f"Generated SQL query failed validation: {str(validation_error)}")
                    return ''

            return result

        except Exception as e:
            print(f"An error occurred while generating the SQL query: {str(e)}")
            return ''

    def sql_query_for_all_rounder_stats(self, query: str, temperature: float = 0.7, top_p: float = 0.9, max_tokens: int = 520):
        """
        This agent generates SQL queries for the all rounder stats of a player.
        
        Table name: men_team_rankings
        Table format:
            | Player | Batting-Bowling Avg Diff | Country | Category |
        
        
        Args:
            query (str): User's query about team rankings.
            db (object): Database connection object for validation (optional, if needed).
            temperature (float): Sampling temperature for LLM response generation.
            top_p (float): Nucleus sampling parameter for LLM.
            max_tokens (int): Maximum number of tokens in the LLM's response.
        
        Returns:
            str: Generated SQL query or an appropriate error message.
        """

        try:
            # Define the system message for query generation

            prompt=f'''
                You are a helpful assistant who generates SQL queries.\n
                The queries should retrieve information from the 'men_allrounder_stats' table, which has the following structure:\n
                | Player | Batting-Bowling Avg Diff | Country | Category |\n
                Write efficient SQL queries based on the user's request, ensuring proper formatting and syntax.\n
                While searching ignore case\n
                Keep in mind to use LIKE for entity names
                Just give the sql query as output\n
                User Query : {query}
            '''

            result = sql_client.predict(
                    user_query=prompt,
                    api_name="/predict"
            )
            print('space result : ')
            print(result)
            
            if db:
                print('inside db')
                try:
                    print('inside try')
                    with db.connect() as connection:
                        result = connection.execute(text(result))  # Executes the SQL query
                        explanation = result.fetchall()  # Fetch the results of EXPLAIN
                        explanation = "\n".join(
                            [f"Player : {row[0]}, Batting-Bowling Avg Diff: {row[1]}, Country: {row[2]}, Category: {row[3]}"
                            for row in explanation]
                        )
                        print(explanation)
                    
                    messages=[
                    
                        {
                            "role": "system",
                            "content": (
                                f"Query : {query}\n"
                                f"Data output : \n{explanation}\n"
                                "The format of the data is as : | Player | Batting-Bowling Avg Diff | Country | Category |\n"
                                "Just answer the query based on the data output in precice words in short."
                            ),
                        },
                    ]

                    response = self.client.chat.completions.create(
                        model="meta-llama/Llama-3.2-3B-Instruct",
                        messages=messages,
                        max_tokens=max_tokens,
                        temperature=temperature,
                        top_p=top_p,
                    )

                    # print(response)

                    # Extract the response content
                    result = response["choices"][0]["message"].get("content", "No content returned.")
                except Exception as validation_error:
                    print(f"Generated SQL query failed validation: {str(validation_error)}")
                    return ''

            return result
            

        except Exception as e:
            print(f"An error occurred while generating the SQL query: {str(e)}")
            return ''

    def sql_query_for_innings_and_match(self, query: str, temperature: float = 0.7, top_p: float = 0.9, max_tokens: int = 520):
        """
        This agent generates SQL queries for the all rounder stats of a player.
        
        Table name: men_team_rankings
        Table format:
            | Innings Player | Innings Runs Scored | Innings Minutes Batted | Innings Batted Flag | Innings Not Out Flag | Innings Balls Faced | Innings Boundary Fours | Innings Boundary Sixes | Innings Batting Strike Rate | Innings Number | Opposition | Ground | Innings Date | Country | 50's | 100's | Innings Runs Scored Buckets | Innings Overs Bowled | Innings Bowled Flag | Innings Maidens Bowled | Innings Runs Conceded | Innings Wickets Taken | 4 Wickets | 5 Wickets | 10 Wickets | Innings Wickets Taken Buckets | Innings Economy Rate | Category |
            | Result | Margin | Match | Home/Away | Ground | Match Date | Matches | Country |
        
        
        Args:
            query (str): User's query about team rankings.
            db (object): Database connection object for validation (optional, if needed).
            temperature (float): Sampling temperature for LLM response generation.
            top_p (float): Nucleus sampling parameter for LLM.
            max_tokens (int): Maximum number of tokens in the LLM's response.
        
        Returns:
            str: Generated SQL query or an appropriate error message.
        """

        try:
            # Define the system message for query generation

            prompt=f'''
                Query: {query} ; Based on query figure out whether to give an answer directly or query the database.

                I have 2 tables:

                1. **Table Name:** 'men_test_innings'  
                **Columns:**  
                | "Innings Player" | "Innings Runs Scored" | "Innings Minutes Batted" | "Innings Batted Flag" | "Innings Not Out Flag" | "Innings Balls Faced" | "Innings Boundary Fours" | "Innings Boundary Sixes" | "Innings Batting Strike Rate" | "Innings Number" | "Opposition" | "Ground" | "Innings Date" | "Country" | "50's" | "100's" | "Innings Runs Scored Buckets" | "Innings Overs Bowled" | "Innings Bowled Flag" | "Innings Maidens Bowled" | "Innings Runs Conceded" | "Innings Wickets Taken" | "4 Wickets" | "5 Wickets" | "10 Wickets" | "Innings Wickets Taken Buckets" | "Innings Economy Rate" | "Category" |

                2. **Table Name:** 'men_test_match_result'  
                **Columns:**  
                | "Result" | "Margin" | "Match" | "Home/Away" | "Ground" | "Match Date" | "Matches" | "Country" |

                **Query Handling:**
                - If the query is about a player, use the `men_test_innings` table.
                - If the query is about match results, use the `men_test_match_result` table.
                - Use **LIKE** for entity names and **LOWER()** to make searches case-insensitive.
                - Ensure all column names with spaces are enclosed in double quotes (`"Column Name"`).
                - For Dates you need to use wilcards with 'LIKE' or convert the column into date and then check
                - Sample Date in the db is like '1877/03/15' or "2010-11-25 00:00:00.000000"

                **Output Requirement:**
                - Generate only the SQL query as output without explanation or formatting errors.
                '''

            result = sql_client.predict(
                    user_query=prompt,
                    api_name="/predict"
            )
            print('space result : ')
            print(result)
            
            if db:
                print('inside db')
                try:
                    print('inside try')
                    with db.connect() as connection:
                        result = connection.execute(text(result))  # Executes the SQL query
                        explanation = result.fetchall()  # Fetch the results of EXPLAIN
                        columns = result.keys()  # Get column names dynamically
                        formatted_output = [dict(zip(columns, row)) for row in explanation]
                        # explanation = "\n".join(
                        #     [f"Player : {row[0]}, Batting-Bowling Avg Diff: {row[1]}, Country: {row[2]}, Category: {row[3]}"
                        #     for row in explanation]
                        # )
                        print(formatted_output)
                        
                    
                    messages=[
                    
                        {
                            "role": "system",
                            "content": (
                                f"Query: {query}\n"
                                f"Answer to the query:\n{formatted_output}\n"
                                # "Summarize the given data accurately based on its type:\n"
                                "- If it's a count, state the numeric value clearly.\n"
                                "- If it's a list of records, extract and present key insights concisely.\n"
                                "- If it's a complex result, structure the response meaningfully.\n"
                                "- Avoid additional context or explanation.\n"
                                "Answer only the essential information."
                            ),
                        },
                    ]

                    response = self.client.chat.completions.create(
                        model="meta-llama/Llama-3.2-3B-Instruct",
                        messages=messages,
                        max_tokens=max_tokens,
                        temperature=temperature,
                        top_p=top_p,
                    )

                    # print(response["choices"][0]["message"].get("content", "No content returned."))

                    # Extract the response content
                    result = response["choices"][0]["message"].get("content", "No content returned.")
                    # result = 'smth'
                except Exception as validation_error:
                    print(f"Generated SQL query failed validation: {str(validation_error)}")
                    return ''

            return result
            
            

        except Exception as e:
            print(f"An error occurred while generating the SQL query: {str(e)}")
            return ''


    # def sql_query_for_

    def process_query(self, query: str) -> str:
        """
        Process user query and return relevant information
        """
        query_lower = query.lower()

        if "rank" and "team" in query_lower:
            return self.sql_query_for_team_ranking(query_lower)

        if "allrounder" in query_lower or "all rounder" in query_lower:
            return self.sql_query_for_all_rounder_stats(query_lower)
        
        if any(word in query_lower for word in {"innings", "batting", "strike rate", "runs", "balls faced", "match"}):
            return self.sql_query_for_innings_and_match(query_lower)
        
        return 'I  not sure about that yet.'

    def chat(self):
        """
        Interactive chat interface
        """
        print("Cricket Bot: Hi! I'm your cricket specialist. I can provide live scores, "
              "player statistics, and rankings!")
        print("Example queries:")
        print("- Show live scores")
        print("- Show stats of Kohli")
        print("- Show ODI rankings")
        print("(Type 'quit' to exit)")
        
        while True:
            user_input = input("You: ").strip()
            
            if user_input.lower() == 'quit':
                print("Cricket Bot: Goodbye!")
                break
            
            response = self.process_query(user_input)
            print(f"Cricket Bot: {response}")

    

# if __name__ == "__main__":
#     bot = CricketWebBot()
#     bot.chat()
    


from flask import Flask, request, jsonify

from flask_cors import CORS


app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

# Initialize the bot
bot = CricketWebBot()

@app.route("/ask-question", methods=["POST"])
def ask_question():
    """
    Flask endpoint to handle chat queries.
    Expects a JSON request: {"query": "Show ODI rankings"}
    Returns the bot's response.
    """
    data = request.json
    query = data.get("question", "")
    if not query:
        return jsonify({"error": "No question provided"}), 400
    
    print(query)
    
    response = bot.process_query(query)  # Using the existing method
    print(response)
    # print(f'response type : {type(response)}')
    # print(jsonify())
    if not response:
        return jsonify({"answer": "An error occured please try again"})
    return jsonify({"answer": response})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
