{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "welcome! Your message to the steps game was: carrots\n"
     ]
    }
   ],
   "source": [
    "import requests\n",
    "a = requests.get('http://52.34.243.66:8080/steps?message=carrots')\n",
    "print(a.content.decode('utf-8'))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd\n",
    "# b=pd.read_json('http://52.34.243.66:8080/steps?message=biscuits')\n",
    "# print(type(b))\n",
    "# print(b)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "welcome! Your message to the steps game was: 42\n",
      "milliseconds: 26.196956634521484\n"
     ]
    }
   ],
   "source": [
    "import requests\n",
    "import time\n",
    "\n",
    "def stepscaller(s): \n",
    "    return requests.get('http://52.34.243.66:8080/steps?message=' + str(s)).text\n",
    "\n",
    "toc = time.time()\n",
    "steps_response = stepscaller(42)\n",
    "tic = time.time()\n",
    "\n",
    "print(steps_response)\n",
    "print('milliseconds:', 1000.*(tic-toc))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "def isprime(n):\n",
    "    if n == 2: return True\n",
    "    if n < 2 or not n % 2: return False\n",
    "    for i in range(3, int(sqrt(n))+1, 2):\n",
    "        if not n % i: return False\n",
    "    return True\n",
    "\n",
    "from math import sqrt\n",
    "n = 39458383751\n",
    "print(isprime(n))"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# The Steps Game\n",
    "\n",
    "You play this game by running the little program given below. \n",
    "The purpose of the program is to talk to a Server. \n",
    "In order for it to work you must have the `requests` library installed on your computer. \n",
    "\n",
    "\n",
    "Each time you send a message to the Server you are trying to guess what it wants to hear.\n",
    "When you guess correctly (hopefully the Server will give you hints) you move on to the next puzzle.\n",
    "\n",
    "\n",
    "## Putting your message together\n",
    "\n",
    "A guess message is a Python *string* with six pieces glued together. \n",
    "The work is done by the program; so you only have to worry about what to say for your actual *guess*.\n",
    "Here is what those six pieces are, if you are interested:\n",
    "\n",
    "\n",
    "- the string `http://` means the message is going out onto the internet\n",
    "- the ip address `54.69.30.193` is the Server's internet address\n",
    "- the addition of `:8080` is a port number. The Server listens on that port.\n",
    "- the addition of `/begin` is the first puzzle game **route**. Each puzzle has an associated route.\n",
    "- the addition of `?message=` is a key. This tells the Server to get ready for your guess.\n",
    "- the addition of your guess (as a string) is the value that goes with the key\n",
    "\n",
    "This is a lot of detail. The point is that this structure gives us a lot of flexibility in how we \n",
    "communicate between two computers. You can also imagine it is a bit like casting a magic spell: \n",
    "It is all necessary for the spell to work... even if the precise details are unclear.\n",
    "\n",
    "\n",
    "## Running the program\n",
    "\n",
    "When you run this code the `input()` statement will prompt you for a message to send the Server\n",
    "on the `begin` route. Once you solve this first puzzle you will be given the next route. To \n",
    "change your route just type in `route` and then enter the new route name. From there you can \n",
    "start working on the second puzzle. \n",
    "\n",
    "\n",
    "To stop playing just type in `exit` or `quit`. \n",
    "\n",
    "## Installing `requests`\n",
    "\n",
    "If you do not have the `requests` module installed you will get an error:\n",
    "\n",
    "\n",
    "`no module named 'requests'`\n",
    "\n",
    "\n",
    "To install it on a PC:\n",
    "\n",
    "- Open the `command` window \n",
    "- Type in the command `python -m pip install requests`\n",
    "- Try the program again to see if `requests` is now ok\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "import requests, time\n",
    "urlbase, route = 'http://54.69.30.193:8080/', 'begin'\n",
    "while True:\n",
    "    msg = input(\"msg to send to route '\" + route + \"':\")\n",
    "    if msg == 'exit' or msg == 'quit':  break\n",
    "    if msg == 'route': route = input(\"enter a new route:\")\n",
    "    else: \n",
    "        tic = time.time()\n",
    "        answer_back = requests.get(urlbase + route + '?' + 'message=' + msg).text\n",
    "        toc = time.time()\n",
    "        print('\\nServer response: \\n\\n' + answer_back + '\\n\\n' + str(round((toc - tic)*1000., 1)) \\\n",
    "              + ' milliseconds, URL = ' + urlbase + route + '?' + 'message=' + msg + '\\n\\n') "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "import requests, time\n",
    "urlbase, route = 'http://54.69.30.193:8080/', 'begin'\n",
    "\n",
    "msg = 'hello' \n",
    "tic = time.time()\n",
    "answer_back = requests.get(urlbase + route + '?' + 'message=' + msg).text\n",
    "toc = time.time()\n",
    "print('\\nServer response: \\n\\n' + answer_back + '\\n\\n' + str(round((toc - tic)*1000., 1)) + ' milliseconds, URL = ' + urlbase + route + '?' + 'message=' + msg + '\\n\\n') "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# join / quit / who / move \n",
    "\n",
    "import requests, time\n",
    "urlbase, route = 'http://54.69.30.193:8080/', 'join'\n",
    "while True:\n",
    "    msg = input(\"msg to send to route '\" + route + \"':\")\n",
    "    if msg == 'exit' or msg == 'quit':  break\n",
    "    if msg == 'route': route = input(\"enter a new route:\")\n",
    "    else:\n",
    "        tic = time.time()\n",
    "        answer_back = requests.get(urlbase + route + '?' + 'name=' + msg).text           # key is hardcoded\n",
    "        toc = time.time()\n",
    "        print('\\nServer response: \\n\\n' + answer_back + '\\n\\n' + str(round((toc - tic)*1000., 1)) \\\n",
    "              + ' milliseconds, URL = ' + urlbase + route + '?' + 'message=' + msg + '\\n\\n') "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "r='hello'\n",
    "s='-7'\n",
    "t='-7.8'\n",
    "u='0'\n",
    "v='7.4'\n",
    "w='9'\n",
    "print(r.isnumeric())\n",
    "print(s.isnumeric())\n",
    "print(t.isnumeric())\n",
    "print(u.isnumeric())\n",
    "print(v.isnumeric())\n",
    "print(w.isnumeric())\n",
    "\n",
    "try:\n",
    "    rfloat = float(r)\n",
    "except: \n",
    "    print('nope:', r)\n",
    "    \n",
    "try:\n",
    "    tfloat = float(t)\n",
    "except:\n",
    "    print('nope', t)\n",
    "\n",
    "\n",
    "print(tfloat, int(tfloat))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {},
   "outputs": [],
   "source": [
    "from ipyturtle import Turtle\n",
    "\n",
    "a = Turtle()\n",
    "a.forward(100)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "application/vnd.jupyter.widget-view+json": {
       "model_id": "db12cb81e8774d48a7c9c205a170e394",
       "version_major": 2,
       "version_minor": 0
      },
      "text/plain": [
       "interactive(children=(IntSlider(value=10, description='x', max=30, min=-10), Output()), _dom_classes=('widget-…"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "from __future__ import print_function\n",
    "from ipywidgets import interact, interactive, fixed, interact_manual\n",
    "import ipywidgets as widgets\n",
    "\n",
    "def f(x): return x\n",
    "\n",
    "interact(f, x=10);"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "metadata": {},
   "outputs": [],
   "source": [
    "a=[[1.,2.]]\n",
    "impulse = (3, 4)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "[[7.0, 10.0]]"
      ]
     },
     "execution_count": 9,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "a[0]+=[4.,5.]\n",
    "a[0]=[a[0][i] + impulse[i] for i in range(2)] \n",
    "a"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.8.5"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
