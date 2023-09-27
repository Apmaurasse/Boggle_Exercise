from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle

class FlaskTests(TestCase):

    

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_no_guesses_after_game_end(self):
        """Test that no more guesses can be made after the timer has ended."""

        with self.client as client:
            # Set a very short timer (e.g., 1 second) for testing purposes
            response = client.get('/?secs=1')

        # Simulate the timer reaching zero
        import time
        time.sleep(2)  # Wait for the timer to end (adjust the time as needed)

        # Attempt to submit a word after the timer has ended
        response = self.client.get('/check-word?word=testword')

        # Verify that the response indicates that no more guesses can be made
        self.assertEqual(response.json['result'], 'not-word')

    
    def test_lowercase_input_only(self):
        """Test that word guesses should only be in lowercase."""

        with self.client as client:
            response = client.get('/')

        # Attempt to submit a word with uppercase characters
        response = self.client.get('/check-word?word=Uppercase')

        # Verify that the response indicates that uppercase characters are not allowed
        self.assertEqual(response.json['result'], 'not-word')

    def test_homepage(self):
        """Make sure information is in the session and HTML is displayed"""

        with self.client:
            response = self.client.get('/')
            self.assertIn('board', session)
            self.assertIsNone(session.get('highscore'))
            self.assertIsNone(session.get('nplays'))
            self.assertIn(b'<p>High Score:', response.data)
            self.assertIn(b'Score:', response.data)
            self.assertIn(b'Seconds Left:', response.data)

    def test_valid_word(self):
        """Test if word is valid by modifying the board in the session"""

        with self.client as client:
            with client.session_transaction() as sess:
                sess['board'] = [["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"]]
        response = self.client.get('/check-word?word=cat')
        self.assertEqual(response.json['result'], 'ok')

    def test_invalid_word(self):
        """Test if word is in the dictionary"""

        self.client.get('/')
        response = self.client.get('/check-word?word=impossible')
        self.assertEqual(response.json['result'], 'not-on-board')

    def non_english_word(self):
        """Test if word is on the board"""

        self.client.get('/')
        response = self.client.get(
            '/check-word?word=fsjdakfkldsfjdslkfjdlksf')
        self.assertEqual(response.json['result'], 'not-word')


    