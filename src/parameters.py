import json


class Parameters:

    def __init__(self):
        self.title = 'New Synth'

        self.attack = .01
        self.decay = .01
        self.sustain = .08
        self.release = .2
        self.volume = .5

        self.hold = True

        self.overtones = [1.0] + 15 * [0]

    def to_dict(self):
        return {
            'title': self.title,
            'attack': self.attack,
            'decay': self.decay,
            'sustain': self.sustain,
            'release': self.release,
            'volume': self.volume,
            'hold': self.hold,
            'overtones': self.overtones,
        }

    def from_dict(self, dictionary):
        self.title = dictionary['title']
        self.attack = dictionary['attack']
        self.decay = dictionary['decay']
        self.sustain = dictionary['sustain']
        self.release = dictionary['release']
        self.volume = dictionary['volume']
        self.hold = dictionary['hold']
        self.overtones = dictionary['overtones']

    @staticmethod
    def create_from_dict(dictionary):
        parameters = Parameters()
        parameters.from_dict(dictionary)
        return parameters

    @staticmethod
    def save_all_parameters(all_parameters):
        with open('resource/data/parameters.json', 'w') as f:
            parameters_list = []
            for parameters in all_parameters:
                parameters_list.append(parameters.to_dict())

            json.dump(parameters_list, f)

    @staticmethod
    def load_all_parameters():
        with open('resource/data/parameters.json', 'r') as f:
            parameter_list = json.load(f)
            all_parameters = []
            for parameter_dict in parameter_list:
                all_parameters.append(Parameters.create_from_dict(parameter_dict))
        return all_parameters

