UCR Schedule Reccomender

- Pulls course information from Banner API and takes in user data on courses they have taken to reccomend a schedule.

Ideas Being Tested
1. Tool Functionality
  - Agent can call tools to access information about courses and CRNs
  - Goal is to reduce the amount of data the agent is given
2. Schedule
  - Rigid schedule that does error checking
  - Goal is to inform agent of errors and reduce the chance it makes them.
  - Prevents invalid schedules from being constructed
  - Checks time conflicts, prereqs
3. Weight-Assignment for Classes
  - Assigns major classees and breadth category a weight or priority
  - Priority is depedent on factors, such as:
      1. Amount of classes the class is a prereq for
      2. Amount of breadth classes vs major classes to be taken
      3. Avalabiality based on quarter and registration trends

Completed:
- AI Agent with Gemini API that assists with registration
- Tool functionaility for course lookup by name (eg. CS010A) and CRN
- Tool functionality for editing a schedule. The schedule can also handle time conflicts just in case the agent

Work In Progress:
- Tool to read in user's courses
- Functionality to convert a transcript into a list of courses the user has taken
- Tool to read in major requirements
- Algorithm that constructs a directed graph of major requirements based on prerequisite.
- Schedule functionaltiy to check for prereq
