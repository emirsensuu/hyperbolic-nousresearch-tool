# 🤖 AI Question-Answer System

An automated system that generates random questions using Hyperbolic's AI and gets answers from various Nous Research models. Perfect for testing and comparing different AI models' responses.

## 💰 Required Costs

Before starting, you'll need to set up accounts with the following services:

- **Hyperbolic**: $10 initial credit
- **Nous Research**: $10 initial credit
- **Railway**: $5/month for Hobby plan ([Sign up with referral link](https://railway.com?referralCode=nok8CN))

## 🌟 Features

- Generates unique questions for each model
- Optimized token usage for cost efficiency
- Automated logging of all interactions
- Cooldown mechanism to prevent rate limiting
- Supports multiple Nous Research models

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Railway account ([Sign up with referral link](https://railway.com?referralCode=nok8CN))
- Hyperbolic API key
- Nous Research API key

### Installation

1. Clone the repository:
```bash
git clone https://github.com/emirsensuu/nous.git
cd nous
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

### Configuration

1. Get your API keys:
   - Hyperbolic API key: [Hyperbolic Platform](https://hyperbolic.xyz) ($10 initial credit)
   - Nous Research API key: [Nous Research Portal](https://portal.nousresearch.com/api-keys) ($10 initial credit)

2. Set up environment variables in Railway:
   - `HYPERBOLIC_API_KEY`: Your Hyperbolic API key
   - `NOUS_API_KEY`: Your Nous Research API key

## 🚂 Railway Deployment

1. Fork this repository to your GitHub account

2. Go to [Railway](https://railway.com?referralCode=nok8CN) and create a new project (requires $5/month Hobby plan)

3. Choose "Deploy from GitHub repo"

4. Select your forked repository

5. Add environment variables:
   - Go to your project's "Settings"
   - Click on "Environment Variables"
   - Add the following variables:
     ```
     HYPERBOLIC_API_KEY=your_hyperbolic_api_key
     NOUS_API_KEY=your_nous_api_key
     ```

6. Deploy your project

## 📝 Usage

The system will:
1. Generate a unique question for each model
2. Ask the question to the selected model
3. Log the interaction
4. Wait for the cooldown period
5. Repeat with the next model

All interactions are displayed in the Railway logs.

## ⚙️ Configuration Options

You can modify these settings in `main.py`:

```python
COOLDOWN_SECONDS = 30  # Time between model interactions
MAX_TOKENS_HYPERBOLIC = 128  # Max tokens for questions
MAX_TOKENS_NOUS = 256  # Max tokens for answers
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Hyperbolic](https://hyperbolic.xyz) for the question generation API
- [Railway](https://railway.com?referralCode=nok8CN) for the deployment platform