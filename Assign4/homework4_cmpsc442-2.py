
############################################################
# CMPSC442: Classification
############################################################

student_name = "Jaden Peacock"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.
import email
from email import policy
from email.iterators import body_line_iterator
import math
from collections import defaultdict
import os

############################################################
# Section 1: Spam Filter
############################################################

def load_tokens(email_path):
    with open(email_path, 'r', encoding='utf-8') as file_obj:
        message = email.message_from_file(file_obj, policy=policy.default)
        tokens = []
        for line in body_line_iterator(message):
            tokens.extend(line.split())
        return tokens

def log_probs(email_paths, smoothing):
    word_counts = defaultdict(int)
    total_words = 0

    # Count words in all emails
    for path in email_paths:
        tokens = load_tokens(path)
        for token in tokens:
            word_counts[token] += 1
            total_words += 1

    # Calculate vocabulary size
    vocab_size = len(word_counts)

    # Calculate log probabilities
    log_probabilities = {}
    for word, count in word_counts.items():
        prob = (count + smoothing) / (total_words + smoothing * (vocab_size + 1))
        log_probabilities[word] = math.log(prob)

    # Calculate log probability for <UNK>
    unk_prob = smoothing / (total_words + smoothing * (vocab_size + 1))
    log_probabilities["<UNK>"] = math.log(unk_prob)

    return log_probabilities

class SpamFilter(object):

    def __init__(self, spam_dir, ham_dir, smoothing):
        # Get all spam and ham email paths
        spam_paths = [os.path.join(spam_dir, fname) for fname in os.listdir(spam_dir)]
        ham_paths = [os.path.join(ham_dir, fname) for fname in os.listdir(ham_dir)]

        # Calculate class probabilities
        self.p_spam = len(spam_paths) / (len(spam_paths) + len(ham_paths))
        self.p_ham = len(ham_paths) / (len(spam_paths) + len(ham_paths))

        # Compute log probabilities for spam and ham
        self.spam_log_probs = log_probs(spam_paths, smoothing)
        self.ham_log_probs = log_probs(ham_paths, smoothing)
    
    def is_spam(self, email_path):
        tokens = load_tokens(email_path)
        spam_score = math.log(self.p_spam)
        ham_score = math.log(self.p_ham)

        for token in tokens:
            if token in self.spam_log_probs:
                spam_score += self.spam_log_probs[token]
            else:
                spam_score += self.spam_log_probs["<UNK>"]

            if token in self.ham_log_probs:
                ham_score += self.ham_log_probs[token]
            else:
                ham_score += self.ham_log_probs["<UNK>"]

        return spam_score > ham_score

    def most_indicative_spam(self, n):
        indicative_words = []
        for word in self.spam_log_probs:
            if word in self.ham_log_probs:
                spam_indication = self.spam_log_probs[word] - math.log(
                    (math.exp(self.spam_log_probs[word]) * self.p_spam + math.exp(
                        self.ham_log_probs[word]) * self.p_ham)
                )
                indicative_words.append((word, spam_indication))

        # Sort by indication value in descending order
        indicative_words.sort(key=lambda x: x[1], reverse=True)
        return [word for word, _ in indicative_words[:n]]

    def most_indicative_ham(self, n):
        indicative_words = []
        for word in self.ham_log_probs:
            if word in self.spam_log_probs:
                ham_indication = self.ham_log_probs[word] - math.log(
                    (math.exp(self.spam_log_probs[word]) * self.p_spam + math.exp(
                        self.ham_log_probs[word]) * self.p_ham)
                )
                indicative_words.append((word, ham_indication))

        # Sort by indication value in descending order
        indicative_words.sort(key=lambda x: x[1], reverse=True)
        return [word for word, _ in indicative_words[:n]]