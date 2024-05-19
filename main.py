import sys
import csv

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, \
    QLineEdit, QLabel, QListWidget, QListWidgetItem


def get_data(search):
    with open('dataset.csv', encoding="utf8") as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')

        data = sorted(reader, key=lambda el: el[5])[:-1][::-1]

        songs = [' – '.join((row[2], row[4])) for row in data if
                 (search in row[2].lower() or search in row[
                     3].lower() or search in row[4].lower())]
        artists = [row[2] for row in data if (
                    search in row[2].lower() or search in row[
                3].lower() or search in row[4].lower())]
        albums = [' – '.join((row[2], row[3])) for row in data if (
                    search in row[2].lower() or search in row[
                3].lower() or search in row[4].lower())]

        return sorted(set(songs)), sorted(set(artists)), sorted(set(albums))


class MusicSearchApp(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # Set up the main layout
        mainLayout = QVBoxLayout()

        self.searchHint = QLabel('Press Enter to search', self)
        mainLayout.addWidget(self.searchHint)

        # Search input field
        self.searchInput = QLineEdit(self)
        self.searchInput.setPlaceholderText('Enter song, artist, or album')
        self.searchInput.returnPressed.connect(self.perform_search)
        mainLayout.addWidget(self.searchInput)

        # Results layout
        resultsLayout = QHBoxLayout()

        # Songs result area
        self.songsList = QListWidget(self)
        self.songsLabel = QLabel('Songs', self)
        self.songsLayout = QVBoxLayout()
        self.songsLayout.addWidget(self.songsLabel)
        self.songsLayout.addWidget(self.songsList)
        resultsLayout.addLayout(self.songsLayout)

        # Artists result area
        self.artistsList = QListWidget(self)
        self.artistsLabel = QLabel('Artists', self)
        self.artistsLayout = QVBoxLayout()
        self.artistsLayout.addWidget(self.artistsLabel)
        self.artistsLayout.addWidget(self.artistsList)
        resultsLayout.addLayout(self.artistsLayout)

        # Albums result area
        self.albumsList = QListWidget(self)
        self.albumsLabel = QLabel('Albums', self)
        self.albumsLayout = QVBoxLayout()
        self.albumsLayout.addWidget(self.albumsLabel)
        self.albumsLayout.addWidget(self.albumsList)
        resultsLayout.addLayout(self.albumsLayout)

        mainLayout.addLayout(resultsLayout)

        # Set main layout
        self.setLayout(mainLayout)

        # Set window properties
        self.setWindowTitle('Music Search')
        self.setGeometry(300, 300, 1080, 720)
        self.show()

    def perform_search(self):
        query = self.searchInput.text().lower()

        songs, artists, albums = get_data(query)

        self.songsList.clear()
        self.artistsList.clear()
        self.albumsList.clear()

        if songs:
            for song in songs:
                self.songsList.addItem(QListWidgetItem(song))
        else:
            self.songsList.addItem(QListWidgetItem('Nothing found'))

        if artists:
            for artist in artists:
                self.artistsList.addItem(QListWidgetItem(artist))
        else:
            self.artistsList.addItem(QListWidgetItem('Nothing found'))

        # Search in albums
        if albums:
            for album in albums:
                self.albumsList.addItem(QListWidgetItem(album))
        else:
            self.albumsList.addItem(QListWidgetItem('Nothing found'))

        self.songsLabel.setText(f'Songs ({len(songs)} found)')
        self.artistsLabel.setText(f'Artists ({len(artists)} found)')
        self.albumsLabel.setText(f'Albums ({len(albums)} found)')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MusicSearchApp()
    sys.exit(app.exec_())
