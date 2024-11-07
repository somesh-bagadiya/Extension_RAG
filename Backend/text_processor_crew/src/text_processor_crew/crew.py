from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool

@CrewBase
class TextProcessorCrew():

  @agent
  def cleaner(self) -> Agent:
    return Agent(
      config=self.agents_config['cleaner'],
      verbose=True
    #   tools=[SerperDevTool()]
    )

  @agent
  def categorizer(self) -> Agent:
    return Agent(
      config=self.agents_config['categorizer'],
      verbose=True
    )

  @task
  def cleaning_task(self) -> Task:
    return Task(
      config=self.tasks_config['cleaning_task'],
	  output_file='output/cleaned_text.txt' # This is the file that will be contain the final report.
    )

  @task
  def categorization_task(self) -> Task:
    return Task(
      config=self.tasks_config['categorization_task'],
      output_file='output/text.txt' # This is the file that will be contain the final report.
    )

  @crew
  def crew(self) -> Crew:
    """Creates the LatestAiDevelopment crew"""
    return Crew(
      agents=self.agents, # Automatically created by the @agent decorator
      tasks=self.tasks, # Automatically created by the @task decorator
    #   process=Process.sequential,
      verbose=True,
    ) 