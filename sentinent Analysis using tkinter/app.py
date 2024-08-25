import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tkinter import *
import tkinter.messagebox
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import os

nltk.download('vader_lexicon')
class analysis_text():
    
    # Centering the window on screen
    def center(self, toplevel):
        toplevel.update_idletasks()
        w = toplevel.winfo_screenwidth()
        h = toplevel.winfo_screenheight()
        size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
        x = w/2 - size[0]/2
        y = h/2 - size[1]/2
        toplevel.geometry("%dx%d+%d+%d" % (size + (x, y)))

    # Handling the close window request
    def callback(self):
        if tkinter.messagebox.askokcancel("Quit", "Do you want to leave?"):
            self.main.destroy()

    # Function to display the results
    def setResult(self, type, res):
        if (type == "neg"):
            self.negativeLabel.configure(text="Negative: " + str(res) + " % \n")
        elif (type == "neu"):
            self.neutralLabel.configure(text="Neutral: " + str(res) + " % \n")
        elif (type == "pos"):
            self.positiveLabel.configure(text="Positive: " + str(res) + " % \n")
    
    # Function to plot sentiment results
    def plot_sentiment(self, sentiment_scores):
        labels = ['Positive', 'Neutral', 'Negative']
        scores = [sentiment_scores['pos'], sentiment_scores['neu'], sentiment_scores['neg']]
        
        plt.bar(labels, scores, color=['green', 'blue', 'red'])
        plt.xlabel('Sentiment')
        plt.ylabel('Score')
        plt.title('Sentiment Analysis Scores')
        plt.show()

    # Function to run sentiment analysis
    def runAnalysis(self):
        try:
            sentences = []
            sentence = self.line.get()
            sentences.append(sentence)
            sid = SentimentIntensityAnalyzer()

            for sentence in sentences:
                ss = sid.polarity_scores(sentence)
                
                # Determine sentiment type
                if ss['compound'] >= 0.05: 
                    self.normalLabel.configure(text="Positive statement!") 
                elif ss['compound'] <= -0.05: 
                    self.normalLabel.configure(text="Negative statement") 
                else: 
                    self.normalLabel.configure(text="Neutral statement") 

                # Display the sentiment scores
                for k in sorted(ss):
                    self.setResult(k, ss[k]*100)
                
                # Save results to file
                with open('results.txt', 'a') as f:
                    f.write(f"Sentence: {sentence}\nScores: {ss}\n\n")

                # Plot sentiment scores
                self.plot_sentiment(ss)

                # Add to history
                self.history.insert(END, f"{sentence}\n")

        except Exception as e:
            tkinter.messagebox.showerror("Error", f"An error occurred: {str(e)}")

    # Reset function to clear fields
    def reset(self):
        self.line.delete(0, END)
        self.typedText.configure(text="")
        self.negativeLabel.configure(text="")
        self.neutralLabel.configure(text="")
        self.positiveLabel.configure(text="")
        self.normalLabel.configure(text="")
        self.history.delete(1.0, END)
        if os.path.exists('results.txt'):
            os.remove('results.txt')

    # Function for real-time text display
    def editedText(self, event):
        self.typedText.configure(text=self.line.get() + event.char)

    # Function to run analysis by pressing Enter
    def runByEnter(self, event):
        self.runAnalysis()

    def __init__(self):
        # Create main window
        self.main = Tk()
        self.main.title("Sentiment Analysis System")
        self.main.geometry("800x700")
        self.main.resizable(width=FALSE, height=FALSE)
        self.main.protocol("WM_DELETE_WINDOW", self.callback)
        self.main.focus()
        self.center(self.main)

        # Input area
        self.label1 = Label(text="Type a text here:")
        self.label1.pack()

        self.line = Entry(self.main, width=70)
        self.line.pack()

        # Real-time typed text display
        self.textLabel = Label(text="\n", font=("Helvetica", 15))
        self.textLabel.pack()
        self.typedText = Label(text="", fg="blue", font=("Helvetica", 20))
        self.typedText.pack()

        self.line.bind("<Key>", self.editedText)
        self.line.bind("<Return>", self.runByEnter)

        # Sentiment analysis results
        self.result = Label(text="\n", font=("Helvetica", 15))
        self.result.pack()
        self.negativeLabel = Label(text="", fg="red", font=("Helvetica", 20))
        self.negativeLabel.pack()
        self.neutralLabel = Label(text="", font=("Helvetica", 20))
        self.neutralLabel.pack()
        self.positiveLabel = Label(text="", fg="green", font=("Helvetica", 20))
        self.positiveLabel.pack()
        self.normalLabel = Label(text="", fg="red", font=("Helvetica", 20))
        self.normalLabel.pack()

        # Text history label
        Label(text="Sentiment History:", font=("Helvetica", 12)).pack()
        self.history = Text(self.main, width=80, height=10, wrap=WORD)
        self.history.pack()

        # Buttons for reset and save
        Button(self.main, text="Reset", command=self.reset, fg="white", bg="blue").pack(side=LEFT, padx=10, pady=10)

# Driver code
myanalysis = analysis_text()
mainloop()