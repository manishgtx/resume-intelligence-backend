from .state import CareerState
from langgraph.graph import StateGraph,START,END
from .nodes.jobDescNode.node import jobDescriptionIngestion
from .nodes.resumeNode.node import resumeIngestion
from .nodes.candidateEvaluationNode.node import candidateEvaluation

# pyrefly: ignore
graph = StateGraph(CareerState)
graph.add_node('resume',resumeIngestion)
graph.add_node('job_desc',jobDescriptionIngestion)
graph.add_node('candidate_evaluation',candidateEvaluation)

# edges
graph.add_edge(START,'resume')
graph.add_edge(START,'job_desc')
graph.add_edge('resume','candidate_evaluation')
graph.add_edge('job_desc','candidate_evaluation')
graph.add_edge('candidate_evaluation',END)

# compile graph
workflow = graph.compile()

# ai_msg=workflow.invoke({"jobDescription":descrption})

# if __name__ == "__main__":
# png = app.get_graph().draw_mermaid_png()

# with open("graph.png", "wb") as f:
#     f.write(png)

# print("Graph generated: graph.png")