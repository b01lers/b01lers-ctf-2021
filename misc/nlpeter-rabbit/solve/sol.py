def plot():
    import nltk
    import matplotlib.pyplot as plt
    f = open("egghunt.txt")
    raw = f.read()
    tokens = nltk.word_tokenize(raw)
    text = nltk.Text(tokens)

    from nltk.draw.dispersion import dispersion_plot
    plt.figure(figsize=(20, 3))
    targets = ['creative', "egg", "hunt", 'happy', 'easter', 'yall']

    dispersion_plot(text, targets, ignore_case=True, title='Lexical Dispersion Plot')

if __name__ == "__main__":
    plot()