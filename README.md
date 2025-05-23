# Facebook AI Auto Responder

This project sets up an AI-powered auto-responder for Facebook comments using Flask, OpenAI, and Facebook Graph API. It can detect the language of comments and reply with a default message if the language is not supported.

## Files
- **app.py**: Main Flask server code handling webhooks, language detection, OpenAI integration, and sending replies to Facebook.
- **requirements.txt**: Python dependencies.
- **Procfile**: Specifies the command for running the app on Render.
- **README.md**: This file.

## Setup

1. **Clone this repository** to your local machine or directly connect to GitHub in Render.

2. **Set Environment Variables** on Render (or your hosting):
   - `PAGE_ACCESS_TOKEN`: Your Facebook Page Access Token.
   - `VERIFY_TOKEN`: A token you choose for webhook verification (e.g., `my_verify_token`).
   - `OPENAI_API_KEY`: Your OpenAI API Key.

3. **Deploy to Render**:
   - Create a new **Web Service** on Render.
   - Connect your GitHub account and select this repository.
   - Set **Build Command**: `pip install -r requirements.txt`
   - Set **Start Command**: `python app.py`
   - Set **Region** to the nearest location (e.g., Singapore for Indonesia).
   - Add the environment variables as listed above.
   - Click **Create Web Service** and wait for deployment to complete.
   - Once deployed, note the URL (e.g., `https://your-app-name.onrender.com`).

4. **Configure Facebook Webhook**:
   - Go to your Facebook Developer Dashboard.
   - Under **Webhook**, click **Add Callback URL**.
   - Enter the deployed URL followed by `/webhook` (e.g., `https://your-app-name.onrender.com/webhook`).
   - Use the same `VERIFY_TOKEN` used in environment variables.
   - Subscribe to **Page** events and select **comments**.
   - Complete webhook setup.

5. **Test**:
   - Post a comment on your Facebook Page.
   - The auto-responder should reply automatically.

## Language Detection
- Comments in Indonesian (`id`) and English (`en`) will be processed by OpenAI.
- Comments in other languages will receive a default reply:
  > Maaf ya, saya belum bisa memahami bahasa itu. Tapi terima kasih sudah berkomentar!

---

Feel free to modify the code to add more features or support additional languages.
