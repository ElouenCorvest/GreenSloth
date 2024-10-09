#!/usr/bin/python3
from smtplib import SMTP_SSL as SMTP       # this invokes the secure SMTP protocol (port 465, uses SSL)
from smtplib import SMTPAuthenticationError
from email.mime.text import MIMEText
from getpass import getpass
from typing import Union


class SMTPMailSender():
    # Setup email notifications

    # Initialise variables
    SMTPserver = None
    USERNAME = None
    PASSWORD = None
    default_sender = None
    default_destination = None
    default_subject = None
    _connection_successful = False  # Flag if the initialisation was successful

    # Run an initial setup
    def __init__(
            self, 
            SMTPserver: str, 
            username: Union[str, None] = None, 
            default_sender: Union[str, None] = None, 
            default_destination: Union[str, None] = None
        ) -> None:
        """Set up an object to easily send emails from using an SMTP server.
        Requires the input of an SMTP server address, username and password.
        The password input will be prompted during the setup.

        Args:
            SMTPserver (str): Address of the SMTP server.
            username (Union[str, None], optional): The senders login user name at the SMTP server. Defaults to None.
            default_sender (Union[str, None], optional): The senders email address. Defaults to the username.
            default_destination (Union[str, None], optional): The email address emails should be send to by default. Defaults to None.
        """
        self.setup(SMTPserver, username = username, default_sender = default_sender, default_destination = default_destination)

    # Setup function for setting any necessary variable and testing the connection
    def setup(
            self,
            SMTPserver: Union[str, None] = None, 
            username: Union[str, None] = None, 
            default_sender: Union[str, None] = None, 
            default_destination: Union[str, None] = None
    ) -> None:
        """Change the settings of the SMTPMailSender.
        If a new username is provided the previous username and password will be reset.

        Args:
            SMTPserver (Union[str, None], optional): Address of the SMTP server. Defaults to None.
            username (Union[str, None], optional): The senders login user name at the SMTP server. Defaults to None.
            default_sender (Union[str, None], optional): The senders email address. Defaults to the username.
            default_destination (Union[str, None], optional): The email address emails should be send to by default. Defaults to None.
        """
        # Initialise the Mail Sender
        # Set the SMTP server
        if SMTPserver is not None:
            self.SMTPserver = SMTPserver

        # Reset the connection if a new username is given
        if username is not None:
            self.USERNAME = None
            self.PASSWORD = None
            self._connection_successful = False

        # Try to set the user login
        while (
            (self.USERNAME is None or self.USERNAME != "")
            and not self._connection_successful
        ):
            # Initialise the username
            if username is None and self.USERNAME is None:
                self.USERNAME = input("EMail Address (leave empty to cancel): ")
            else:
                self.USERNAME = username

            # Set the default_sender
            if default_sender is None and self.default_sender is None:
                self.default_sender = self.USERNAME

            # Set the default_destination
            if default_destination is not None:
                self.default_destination = default_destination

            # If no username is given, abort initialisation
            if self.USERNAME == "":
                self.reset()
                pass
            else:
                # Get the password
                self.PASSWORD = getpass(
                    "EMail Password (leave empty to cancel): "
                )

                if self.PASSWORD == "":
                    print("Aborted")
                    self.reset()
                    break
                # Try the connection
                try:
                    with SMTP(self.SMTPserver) as conn:
                        conn.set_debuglevel(False)
                        conn.login(self.USERNAME, self.PASSWORD)
                        conn.quit()
                    self._connection_successful = True
                except SMTPAuthenticationError:
                    print("Login Error, please try again")
    
    # Function for sending emails
    def send_email(
            self, 
            body: str, 
            subject: Union[str, None] = None, 
            destination: Union[str, None] = None,
            sender: Union[str, None] = None,
            text_subtype: str = "plain", 
        ):
        """Send an email. Uses 'default_' arguments by default if they were set previously.
        Doesn't attempt sending and returns None if no username was set.

        Args:
            body (str): Body of the email.
            subject (Union[str, None], optional): Subject line of the email. Defaults to the initialised default_subject.
            destination (Union[str, None], optional): Destination email address of the email. Defaults to the initialised default_destination.
            sender (Union[str, None], optional): Sender email address. Defaults to the initialised default_sender.
            text_subtype (str, optional): MIMEText type of the body. Defaults to "plain".

        Raises:
            ValueError: _description_
            ValueError: _description_
            ValueError: _description_
            ValueError: _description_
        """
        # Just return None if no username was set in the beginning
        if self.USERNAME is None:
            return None

        if not self._connection_successful:
            raise ValueError("Previous connection attempts were unsuccessful, please run setup method")

        # Set the subject
        if subject is None and self.default_subject is None:
            raise ValueError("Please provide a subject line")
        elif subject is None:
            subject = self.default_subject

        # Set the destination
        if destination is None and self.default_destination is None:
            raise ValueError("Please provide a destination")
        elif destination is None:
            destination = self.default_destination
        
        # Set the sender
        if sender is None and self.default_sender is None:
            raise ValueError("Please provide a sender")
        elif sender is None:
            sender = self.default_sender

        # Create the email
        msg = MIMEText(body, text_subtype)
        msg['Subject'] = subject
        msg['From'] = sender  # some SMTP servers will do this automatically, not all

        with SMTP(self.SMTPserver) as conn:
            conn.set_debuglevel(False)
            conn.login(self.USERNAME, self.PASSWORD)

            try:
                conn.sendmail(sender, destination, msg.as_string())
            finally:
                conn.quit()

    def reset(self):
        """Reset the SMTPMailSender"""
        # Reset all variables
        self.SMTPserver = None
        self.USERNAME = None
        self.PASSWORD = None
        self.default_sender = None
        self.default_destination = None
        self.default_subject = None
        self._connection_successful = False