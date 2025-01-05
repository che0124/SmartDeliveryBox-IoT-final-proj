# IoT SmartDeliveryBox
A secure and intelligent delivery management system leveraging IoT technology to revolutionize the delivery experience. This solution combines electronic access control with a web-based interface to provide a seamless, secure platform for managing deliveries.

## 📊 System Architecture
![SmartDeliveryBox system](img/system-diagram.png)

## 🌟 Features
- **OTP Verification for Delivery Personnel** : Use a one-time password (OTP) for secure access.
- **LCD Display for Delivery Personnel** : An LCD screen provides clearly instructions and feedback.
- **Group Access Management** : Allowing multiple people to control the same box.
- **Secure Lock Control** : Electronic lock supports control via the web interface.
- **User-Friendly Operation** : Operated through a web-based interface.

## Workflow
1. **Food Delivery**:  
   Delivery personnel enters a One-Time Password (OTP) on the web interface or a dedicated app to unlock the box and place the food securely.  
   
2. **Real-Time Feedback**:  
   Instructions and box status are displayed on the LCD screen connected to the Raspberry Pi, providing immediate feedback during the delivery process.

3. **Remote Management**:  
   Users (customers) can remotely manage access permissions, monitor delivery status, and lock/unlock the box via the web interface.

4. **Shared Access**:  
   Authorized group members can access the box if granted specific permissions by the primary user.

5. **Hardware Integration**:  
   The Raspberry Pi server controls the hardware components, including the locking mechanism, relay, and LCD, ensuring seamless interaction between software and hardware.

## 📋 Prerequisites
Before beginning the installation, ensure you have the following:
### Hardware Requirements
- **Raspberry Pi**
- **[LY-03 DC12V Electronic Lock](https://www.icshop.com.tw/products/368011000480)**
- **[5V Single Channel Relay Module](https://www.taiwaniot.com.tw/product/1%e8%b7%af%e7%b9%bc%e9%9b%bb%e5%99%a8%e6%a8%a1%e7%b5%84-5v%e4%bd%8e%e9%9b%bb%e5%b9%b3%e8%a7%b8%e7%99%bc-%e7%b9%bc%e9%9b%bb%e5%99%a8%e6%93%b4%e5%b1%95%e6%9d%bf-%e8%97%8d%e7%89%88/)**
- **[I2C 1602 LCD Module with Blue Backlight](https://www.taiwaniot.com.tw/product/1602-%e8%97%8d%e5%ba%95%e7%99%bd%e5%ad%97-iici2c-6x2-%e8%83%8c%e5%85%89%e6%b6%b2%e6%99%b6%e6%a8%a1%e7%b5%84/)**
- **12V Power Supply (Two 6V battery packs in series)**

### Software Requirements
- Python 3.x
- Firebase account with a configured project

---

## 🚀 Quick Start Guide
### Wiring Instructions
1. Power Supply Configuration
   ```bash
   - Connect two 6V battery packs:
     Battery Pack 1 (+) → Battery Pack 2 (-)
     Battery Pack 1 (-) → Lock Negative (-)
     Battery Pack 2 (+) → Relay NO (Normally Open)
   ```
2. Electronic Lock Wiring
   ```bash
   - Lock Positive (+) → Relay COM (Common)
   - Lock Negative (-) → Battery Pack 1 (-)
   ```
3. Relay Module Connections
   ```bash
   - VCC → Raspberry Pi 5V (Pin 2)
   - GND → Raspberry Pi GND (Pin 6)
   - IN  → Raspberry Pi GPIO14 (Pin 8)
   ```

### Circuit Diagram
  ![SmartDeliveryBox Circuit](img/circuit-diagram.png)

### Software Installation
#### For Raspberry Pi
1. Clone the Raspberry Pi repository:
   ```bash
   git clone https://github.com/che0124/iot-SmartDeliveryBox-RaspberryPi.git
   ```
2. Install dependencies:
   ```bash
   cd Siot-SmartDeliveryBox-RaspberryPi
   pip install -r requirements.txt
   ```
3. Run the program:
   ```bash
   python app.py
   ```

#### For Web Server (Computer)
1. Clone the repository:
   ```bash
   git clone https://github.com/che0124/iot-final_proj.git
   ```
2. Install dependencies:
   ```bash
   cd iot-final_proj
   pip install -r requirements.txt
   ```
3. Start the server:
   ```bash
   python app.py
   ```
4. Open `http://localhost:5000` in a browser to access the interface.



## 📄 File Structure

```plaintext
SmartDeliveryBox/
├── app.py            # Main application entry point
├── requirements.txt  # Dependency requirements
├── templates/        # HTML files
├── static/           # Static resources (CSS, JS, Images)
└── README.md         # Documentation

SmartDeliveryBox-Pi/
├── pi_app.py         # Raspberry Pi application entry point
├── requirements.txt  # Dependency requirements
└── README.md         # Documentation
```

---

## 🛡 Security and Privacy
- All data transmission is encrypted to ensure user privacy.

---

## 🤝 Contributing
We welcome contributions from everyone:
1. Fork the repository.
2. Submit a Pull Request.
3. Provide feedback or report issues via [Issues](https://github.com/yourusername/SmartDeliveryBox/issues).

---

## 📧 Contact
For any questions or suggestions, please contact:
- Author: Zhe-Wei Kang
- Email: example@example.com

---

## 📜 License
This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).
