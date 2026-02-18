# Deploying Marketing Chatbot on AWS EC2

This guide outlines how to deploy your Flask application to an AWS EC2 instance using Ubuntu, Gunicorn, and Nginx.

## Prerequisites
- An AWS Account.
- Basic familiarity with the terminal.

## Step 1: Launch an EC2 Instance
1.  **Log in to AWS Console** and go to **EC2**.
2.  Click **Launch Instance**.
3.  **Name**: `MarketingChatbot`.
4.  **OS Image**: Ubuntu Server 24.04 LTS (Free Tier eligible).
5.  **Instance Type**: `t2.micro` (Free Tier) or `t3.small` (Recommended for better performance).
6.  **Key Pair**: Create a new key pair (e.g., `chatbot-key`), download the `.pem` file, and keep it safe.
7.  **Network Settings**:
    -   Check "Allow SSH traffic from Anywhere" (or My IP).
    -   Check "Allow HTTP traffic from the internet".
    -   Check "Allow HTTPS traffic from the internet".
8.  Click **Launch Instance**.

## Step 2: Connect to your Instance
1.  Open your terminal/command prompt.
2.  Locate your `.pem` file.
3.  Run: `ssh -i "path/to/chatbot-key.pem" ubuntu@<your-ec2-public-ip>`

## Step 3: Server Setup
Update the server and install necessary packages:

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install python3-pip python3-venv nginx git -y
```

## Step 4: Clone/Upload Project
You can clone your git repository:

```bash
git clone <your-repository-url>
cd marketing_chatbot
```

*Alternatively, if your code isn't on Git yet, you can use SFTP (FileZilla) or `scp` to upload the `marketing_chatbot` folder to `/home/ubuntu/`.*

## Step 5: Python Environment Setup
Navigate to the backend directory and set up the virtual environment:

```bash
cd marketing_chatbot/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn
```

**Important**: Creates a `.env` file with your API keys:
```bash
nano .env
```
Paste your execution keys inside (`PINECONE_API_KEY`, `GROQ_API_KEY`, etc.), then save (`Ctrl+O`, `Enter`, `Ctrl+X`).

## Step 6: Create Systemd Service
This ensures your app runs in the background and restarts on reboot.

1.  Create the service file:
    ```bash
    sudo nano /etc/systemd/system/chatbot.service
    ```

2.  Paste the following (adjust paths if needed):
    ```ini
    [Unit]
    Description=Gunicorn instance to serve Marketing Chatbot
    After=network.target

    [Service]
    User=ubuntu
    Group=www-data
    WorkingDirectory=/home/ubuntu/marketing_chatbot/backend
    Environment="PATH=/home/ubuntu/marketing_chatbot/backend/venv/bin"
    ExecStart=/home/ubuntu/marketing_chatbot/backend/venv/bin/gunicorn --workers 3 --bind unix:chatbot.sock -m 007 app:app

    [Install]
    WantedBy=multi-user.target
    ```

3.  Start and enable the service:
    ```bash
    sudo systemctl start chatbot
    sudo systemctl enable chatbot
    sudo systemctl status chatbot
    ```

## Step 7: Configure Nginx
Nginx acts as a reverse proxy, forwarding web traffic to Gunicorn.

1.  Create an Nginx config file:
    ```bash
    sudo nano /etc/nginx/sites-available/chatbot
    ```

2.  Paste the following (replace `your_server_ip` with your EC2 Public IP):
    ```nginx
    server {
        listen 80;
        server_name your_server_ip;

        location / {
            include proxy_params;
            proxy_pass http://unix:/home/ubuntu/marketing_chatbot/backend/chatbot.sock;
        }

        # Serve static files directly (Optional optimization)
        location /static/ {
            alias /home/ubuntu/marketing_chatbot/frontend/static/;
        }
    }
    ```

3.  Enable the site and restart Nginx:
    ```bash
    sudo ln -s /etc/nginx/sites-available/chatbot /etc/nginx/sites-enabled
    sudo nginx -t
    sudo systemctl restart nginx
    ```

## Step 8: Access Your App
Open your browser and visit: `http://<your-ec2-public-ip>`

## Step 9: Add SSL (HTTPS)
If you have a customized domain pointing to this IP:

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com
```
