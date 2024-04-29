## Step to run Chat With Webs application
- Clone chat-with-webs in your local machine
- Download and install Anaconda from https://www.anaconda.com/download
- Type anaconda on windows search and open anaconda command prompt
- Navigate to chat-with-webs progect (in step 1) from conda prompt and/by follow below commands
    * cd <basepath>/chat-with-webs
    * conda create -n chat-with-webs python=3.11 -y
    * conda activate chat-with-webs
    * pip install -r requirement.txt
- Create a file with name '.env' in chat-with-webs folder
- Add below line in .env file
    * OPENAI_API_KEY="Supply your secret token here"
- Run Multiple PDF File Reader with below command
    * streamlit run app.py --server.port 8080
- Open http://localhost:8080/ on your favorite browser
    * Upload any number of pdf files and ask question related to that
