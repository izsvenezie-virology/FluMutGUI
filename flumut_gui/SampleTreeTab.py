import sys
from PyQt5.QtWidgets import QApplication, QTreeWidgetItem, QTreeWidget


class SampleTreeTab(QTreeWidget):
    def __init__(self):
        super().__init__()
        data = {
            "sample 1": {
                "marker 1": {
                    "effect 1": {
                        "subtype 1": ["paper A", "paper B"],
                        "subtype 2": ["paper C", "paper D"],
                    },
                    "effect 2": {
                        "subtype 3": ["paper E", "paper F"],
                        "subtype 4": ["paper G", "paper H"],
                    }
                },
                "marker 2": {
                    "effect 3": {
                        "subtype 5": ["paper I", "paper J"],
                        "subtype 6": ["paper K", "paper L"],
                    },
                    "effect 4": {
                        "subtype 7": ["paper M", "paper N"],
                        "subtype 8": ["paper O", "paper P"],
                    }
                }
            },
            "sample 2": {
                "marker 3": {
                    "effect 5": {
                        "subtype 9": ["paper Q", "paper R"],
                        "subtype 10": ["paper S", "paper T"],
                    },
                    "effect 6": {
                        "subtype 11": ["paper U", "paper V"],
                        "subtype 12": ["paper W", "paper X"],
                    }
                },
                "marker 4": {
                    "effect 7": {
                        "subtype 13": ["paper Y", "paper Z"],
                        "subtype 14": ["paper AA", "paper AB"],
                    },
                    "effect 8": {
                        "subtype 15": ["paper AC", "paper AD"],
                        "subtype 16": ["paper AE", "paper AF"],
                    }
                }
            }
        }

        self.setHeaderLabels(["Sample", "Marker", "Effect", "Subtype", "Paper"])
        self.setColumnCount(5)

        top_level_nodes = []
        for sample, markers in data.items():
            sample_node = QTreeWidgetItem([sample, "", "", "", ""])

            for marker, effects in markers.items():
                marker_node = QTreeWidgetItem(["", marker, "", "", ""])

                for effect, subtypes in effects.items():
                    effect_node = QTreeWidgetItem(["", "", effect, "", ""])

                    for subtype, papers in subtypes.items():
                        subtype_node = QTreeWidgetItem(["", "", "", subtype, ""])

                        for paper in papers:
                            paper_node = QTreeWidgetItem(["", "", "", "", paper])
                            subtype_node.addChild(paper_node)

                        effect_node.addChild(subtype_node)
                    marker_node.addChild(effect_node)
                sample_node.addChild(marker_node)
                
            top_level_nodes.append(sample_node)

            self.addTopLevelItems(top_level_nodes)
