import pandas as pd
import networkx as nx


def create_career_graph(data):
    """
    Create a graph connecting careers with their required skills.
    """

    graph = nx.Graph()

    for _, row in data.iterrows():
        career = row["Job_Role"]
        skill = row["Skill"]

        graph.add_node(career, type="career")
        graph.add_node(skill, type="skill")

        graph.add_edge(career, skill)

    return graph


# Load career dataset
data = pd.read_csv("../data/career_data.csv")


# Create career graph
career_graph = create_career_graph(data)


print("Career Graph Created")
print("--------------------")

print("Number of Nodes:", career_graph.number_of_nodes())
print("Number of Edges:", career_graph.number_of_edges())


print("\nCareer Connections:")

for career in data["Job_Role"].unique():
    skills = list(career_graph.neighbors(career))

    print(f"\n{career}:")
    print(skills)