# Carboon Server

Carboon is a prototype application to have a virtual banking system combined with a biometric voice authentication mechanism.
It is depend on IBM Watson technology and piwho to recognise the speaker.

# Dependencies
As it uses piwho to speaker recognition, JDK version 6.0+ needs to be installed on the system
These python libraries are the requirements
  * bottle
  * requests
  * watson-developer-cloud
  * pyaudio
  * piwho
  
# Install
To install just run these command:

```bash
> sudo apt-get install gcc g++ python-dev portaudio19-dev libyaml-dev 
> sudo pip install -r requirements.txt
> git clone https://github.com/Adirockzz95/Piwho.git
> cd Piwho
> sudo python setpu.py install
```

# Usage

After installing requirements you need to run the following command:

```bash
> python3 main.py
```
