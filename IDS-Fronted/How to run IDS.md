
# IDS and Frontend Setup Instructions
This guide provides instructions to set up and run the IDS and its frontend 


## Step 1: Install Node.js and Vue.js
First, update the package lists and install Node.js and npm:

```bash
sudo apt update
sudo apt install nodejs npm
```

Next, install Vue CLI globally:

```bash
sudo npm install -g @vue/cli
```

## Step 2: Install Python Dependencies

Create a virtual environment for Python and install the dependencies from `requirements.txt`:

```bash
sudo apt install python3-venv
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

## Step 3: Run IDS

To start the IDS, run the following command in your virtual environment:

```bash
python3 IDS2.0.py
```

## Step 4: Run Frontend

In a new terminal window, start the Vue.js frontend development server:

```bash
npm run serve
```

Once started, the frontend will be accessible at `http://localhost:8080`.

---

Follow these steps, and the IDS along with its frontend should be up and running.
