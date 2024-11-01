# EmailByTimerCrypted

A Python-based automated email sender with Tor integration for anonymized email delivery. This tool allows users to schedule and send emails at set intervals, with the option to attach images, using a modern GUI. 

## Features

- **Automated Email Sending**: Set up scheduled email sending at custom intervals.
- **Tor Integration**: Uses Tor proxy for anonymized email sending (if configured).
- **Image Attachment**: Option to attach an image to each email.
- **Randomized Subjects**: Prevents email threading by randomizing the subject line.
- **Dark Mode GUI**: Modern, user-friendly interface inspired by contemporary design standards.

## Installation

### Requirements

1. Python 3.7 or higher
2. Required Python packages
   ```bash
   pip install -r requirements.txt
   ```
3. [Tor Browser](https://www.torproject.org/download/)

### Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/RoeyBenHarushDev/NonStopEmails.git
   cd NonStopEmails
   ```

2. **Install Python Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Tor Configuration**: Ensure Tor is installed and running on port `9050` for proxy support.

## Usage

1. **Run the Application**
   ```bash
   python EmailByTimerCrypted.py
   ```

2. **GUI Interface**:
   - Enter recipient email addresses in the `To`, `Cc`, and `Bcc` fields.
   - Set the subject and email body content.
   - Optionally, click `Attach Image` to include an image in the email.
   - Click `Send Email` to start automated sending.
   - Click `Stop Sending` to halt email sending.

3. **Tor Integration**:
   - If Tor is running, the application attempts to use it for anonymity.
   - If Tor is not active, the application will send directly without proxy.

## Configuration

- **Email Settings**: Update `EMAIL_ADDRESS` and `EMAIL_PASSWORD` in the code to your email credentials.
- **Interval Timing**: Adjust the `time.sleep(0.5)` line in the `send_loop` function to change the sending frequency.

## Troubleshooting

- **Tor Connection Error**: Ensure Tor is installed, running, and configured on port `9050`.
- **SMTP Authentication Error**: Confirm that email credentials are correct and that third-party app access is enabled for the email account.
- **Icon Replacement**: To customize the executable icon, specify the path to your `.ico` file in the `pyinstaller` command.

## License

This project is licensed under the MIT License.
