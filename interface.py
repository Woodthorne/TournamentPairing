from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLayout,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget
)

from logic import Logic
from player import Player


class Window(QMainWindow):
    def __init__(self, bll: Logic):
        super(Window, self).__init__()
        self._bll = bll
        
        self.setWindowTitle('Tournament Organizer')
        # self.layout().setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)
        
        self.switch_menu(Registration)
    
    def switch_menu(self, menu_class: 'Menu', **kwargs) -> None:
        self.setCentralWidget(menu_class(self, self._bll, **kwargs))


class Menu(QWidget):
    def __init__(self, root: Window, bll: Logic):
        super().__init__()
        self._root = root
        self._bll = bll


class Registration(Menu):
    def __init__(self, root, bll):
        super().__init__(root, bll)
    
        group = QGroupBox('Registration')
        name_scroll = self._create_name_area()
        inputs = self._create_inputs()
        
        group_layout = QVBoxLayout()
        group_layout.addWidget(name_scroll)
        group_layout.addWidget(inputs)
        group.setLayout(group_layout)

        layout = QVBoxLayout()
        layout.addWidget(group)
        self.setLayout(layout)

    def _create_name_area(self) -> QScrollArea:
        scroll = QScrollArea()
        self.names = QWidget()
        self.names.setLayout(QVBoxLayout())
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll.setWidget(self.names)
        scroll.setMinimumHeight(190)
        # scroll.setFixedHeight(350)
        return scroll
    
    def _create_name_input(self) -> QWidget:
        name_input = QWidget()
        self._input_field = QLineEdit()
        self._input_field.setPlaceholderText('Name')
        self._input_field.returnPressed.connect(self._add_player)
        button = QPushButton('Register')
        button.pressed.connect(self._add_player)

        layout = QHBoxLayout()
        layout.addWidget(self._input_field)
        layout.addWidget(button)
        name_input.setLayout(layout)
        return name_input

    def _create_tournament_start(self) -> QWidget:
        tournament_start = QWidget()
        self._player_total = QLabel('0')
        button = QPushButton('Start')
        button.pressed.connect(self._start_tournament)

        layout = QHBoxLayout()
        layout.addWidget(self._player_total)
        layout.addWidget(button)
        tournament_start.setLayout(layout)
        return tournament_start

    def _create_inputs(self) -> QWidget:
        inputs = QWidget()

        self._name_field = QLineEdit()
        self._name_field.setPlaceholderText('Name')
        self._name_field.returnPressed.connect(self._add_player)
        name_button = QPushButton('Register')
        name_button.pressed.connect(self._add_player)
        self._player_total = QLabel('Players: 0')
        tournament_button = QPushButton('Start')
        tournament_button.pressed.connect(self._start_tournament)

        layout = QGridLayout()
        layout.addWidget(self._name_field, 0, 0)
        layout.addWidget(name_button, 0, 1)
        layout.addWidget(self._player_total, 1, 0)
        layout.addWidget(tournament_button, 1, 1)

        inputs.setLayout(layout)
        return inputs
    
    def _add_player(self) -> None:
        name = self._name_field.text()
        if not name:
            return
        if self._bll.add_player(name):
            player_total = int(self._player_total.text().split()[-1]) + 1
            self._player_total.setText(f'Players: {player_total}')
            label = QLabel(name)
            self.names.layout().addWidget(label)
            label.show()
            self.names.adjustSize()
            # self.names.updateGeometry()
        self._name_field.setText('')
    
    def _start_tournament(self) -> None:
        if self._bll.next_round():
            self._root.switch_menu(TournamentRound)


class TournamentRound(Menu):
    def __init__(self, root, bll):
        super().__init__(root, bll)
        
        group = QGroupBox(f'Round {self._bll.round}')
        pairing_scroll = self._create_pairing_list()
        end_button = QPushButton('End Round')
        end_button.pressed.connect(self._end_round)
        
        group_layout = QVBoxLayout()
        group_layout.addWidget(pairing_scroll)
        group_layout.addWidget(end_button)
        group.setLayout(group_layout)

        layout = QVBoxLayout()
        layout.addWidget(group)
        self.setLayout(layout)

    def _create_pairing_list(self) -> QWidget:
        pairings = self._bll.true_create_pairings()
        self.matches = len(pairings)
        self.results: dict[tuple[Player, Player], tuple[int, int]] = {}
        self.confirmed_results = 0

        scroll = QScrollArea()
        self.pairings = QWidget()
        widget_tuples: list[tuple[QLabel, QLineEdit, QLabel, QLineEdit, QPushButton]] = []
        for player_1, player_2 in pairings:
            widget_tuples.append(self._create_pairing_row(player_1, player_2))

        pairing_layout = QGridLayout()
        for r_index, widgets in enumerate(widget_tuples):
            for c_index, widget in enumerate(widgets):
                pairing_layout.addWidget(widget, r_index, c_index)

        self.pairings.setLayout(pairing_layout)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setWidget(self.pairings)
        scroll.setMinimumHeight(190)
        return scroll
    
    def _create_pairing_row(self, player_1: Player, player_2: Player) -> tuple[QLabel, QLineEdit, QLabel, QLineEdit, QPushButton]:
        label_1 = QLabel(player_1.name)
        input_1 = QLineEdit()
        input_1.setMaxLength(1)
        input_1.setMaximumWidth(20)

        label_2 = QLabel(player_2.name)
        input_2 = QLineEdit()
        input_2.setMaxLength(1)
        input_2.setMaximumWidth(20)
        
        button = QPushButton('Confirm')
        
        def _confirm_results() -> None:
            if input_1.text().isnumeric() and input_2.text().isnumeric():
                print(input_1.text(), input_2.text())
                self.results[(player_1,  player_2)] = (int(input_1.text()), int(input_2.text()))
                if button.text() == 'Confirm':
                    self.confirmed_results += 1
                    button.setText('Update')
                    button.show()
        
        button.pressed.connect(_confirm_results)

        return (label_1, input_1, label_2, input_2, button)

    def _end_round(self) -> None:
        if self.confirmed_results == self.matches:
            self._bll.end_round(self.results)
            self._root.switch_menu(Standings)

class Standings(Menu):
    def __init__(self, root, bll):
        super().__init__(root, bll)

        group = QGroupBox(f'Round {self._bll.round} - Standings')
        ranking_list = self._create_ranking_list()
        next_button = QPushButton('Next Round')
        next_button.pressed.connect(self._next_round)
        
        group_layout = QVBoxLayout()
        group_layout.addWidget(ranking_list)
        group_layout.addWidget(next_button)
        group.setLayout(group_layout)

        layout = QVBoxLayout()
        layout.addWidget(group)
        self.setLayout(layout)
        
    def _create_ranking_list(self) -> QWidget:
        ranked_players = self._bll.get_rankings()

        scroll = QScrollArea()
        
        player_list = QWidget()
        player_tuples: list[tuple[QLabel, QLabel, QLabel, QLabel]] = []
        for index, player in enumerate(ranked_players):
            rank = QLabel(str(index + 1))
            name = QLabel(player.name)
            score = QLabel(str(player.score))
            opp_score = QLabel(str(player.opponents_score()))
            player_tuples.append((rank, name, score, opp_score))

        player_layout = QGridLayout()
        for r_index, widgets in enumerate(player_tuples):
            for c_index, widget in enumerate(widgets):
                player_layout.addWidget(widget, r_index, c_index)

        player_list.setLayout(player_layout)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setWidget(player_list)
        scroll.setMinimumHeight(190)
        return scroll

    def _next_round(self) -> None:
        if self._bll.next_round():
            self._root.switch_menu(TournamentRound)
        else:
            self._root.switch_menu(EndView)
            # for player in self._bll.get_rankings():
            #     print(player, player.opponents)

class EndView(Menu):
    def __init__(self, root, bll):
        super().__init__(root, bll)

        group = QGroupBox(f'Tournament Ended - Standings')
        ranking_list = self._create_ranking_list()
        
        group_layout = QVBoxLayout()
        group_layout.addWidget(ranking_list)
        group.setLayout(group_layout)

        layout = QVBoxLayout()
        layout.addWidget(group)
        self.setLayout(layout)
        
    def _create_ranking_list(self) -> QWidget:
        ranked_players = self._bll.get_rankings()

        scroll = QScrollArea()
        
        player_list = QWidget()
        player_tuples: list[tuple[QLabel, QLabel, QLabel, QLabel]] = []
        for index, player in enumerate(ranked_players):
            rank = QLabel(str(index + 1))
            name = QLabel(player.name)
            score = QLabel(str(player.score))
            opp_score = QLabel(str(player.opponents_score()))
            player_tuples.append((rank, name, score, opp_score))

        player_layout = QGridLayout()
        for r_index, widgets in enumerate(player_tuples):
            for c_index, widget in enumerate(widgets):
                player_layout.addWidget(widget, r_index, c_index)

        player_list.setLayout(player_layout)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setWidget(player_list)
        scroll.setMinimumHeight(190)
        return scroll