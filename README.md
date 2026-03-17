# AGEent.
**Your personal agent for the government 'maze'.**

---

## OVERVIEW
AGEent. is a digital assistant designed to help seniors navigate complex government bureaucracy. It transforms cluttered and difficult-to-read portals into a simple, voice-first conversational experience. The mission is to ensure benefits earned by seniors are accessible through a simple conversation.

## THE PROBLEM
Most government websites for Medicare, Social Security, and the DMV are built with complex structures, small fonts, and confusing terminology. This creates a digital barrier for older adults, often leading to missed benefits or total dependence on others for basic paperwork.

## KEY FEATURES
* **Accessibility-First UI**: High-contrast color palette and dynamic font scaling (A+/A-) for users with visual impairments.
* **Voice Interaction**: Speech-to-text integration using **Nova Sonic** for hands-free navigation.
* **Agentic Automation**: AI-driven form completion powered by **Nova Act** to handle tedious data entry.
* **Secure Authentication**: A multi-step registration and security protocol modeled after **Login.gov** standards.

## TECH STACK
* **Frontend**: Next.js, Tailwind CSS, Lucide Icons.
* **Backend**: FastAPI (Python), PostgreSQL.
* **AI Engine**: Amazon Bedrock (Nova Lite, Nova Sonic, Nova Act).

## SETUP

### Frontend
1. Enter the directory: `cd frontend`
2. Install dependencies: `npm install`
3. Start the server: `npm run dev`
4. Access at: `http://localhost:3000`

### Backend
1. Enter the directory: `cd backend`
2. Create a virtual environment: `python3 -m venv venv`
3. Activate the environment: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Start the API: `uvicorn main:app --reload --port 8000`

## DEMO WORKFLOW
1. **Onboarding**: The user creates an account and selects a secure authentication method such as Face/Touch unlock or Security key.
2. **The Inquiry**: On the home screen, the user taps the microphone and asks a question about Medicare applications.
3. **AI Processing**: The system converts speech to text, retrieves relevant information, and displays it in a large, readable format.
4. **Voice Output**: The AI reads the response aloud to ensure the user understands the next steps.
5. **Automation**: After the user provides data, the agent begins filling out the official government form in the background.
