# chat-with-webs
Chat with any website using Python and Langchain 
## Step to run Chat With Webs application
- Clone chat-with-webs in your local machine
- Download and install Anaconda from https://www.anaconda.com/download
- Type anaconda on windows search and open anaconda command prompt
- Navigate to chat-with-webs progect (in step 1) from conda prompt and/by follow below commands
    * cd <basepath>/chat-with-webs
    * conda create -n chat-with-webs python=3.11 -y
    * conda activate chat-with-webs
    * pip install -r requirement.txt
- Create a file with name '.env' in multi-pdf-reader folder
- Add below line in .env file
    * HUGGINGFACEHUB_API_TOKEN="Supply your secret token here"
- Run Multiple PDF File Reader with below command
    * streamlit run app.py --server.port 8080
- Open http://localhost:8080/ on your favorite browser
    * Upload any number of pdf files and ask question related to that
