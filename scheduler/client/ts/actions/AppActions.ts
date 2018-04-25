// There aren't too many actions for this app, so everything can be held here.

import { alt } from "../alt";
import { AbstractActions } from "./AbstractActions";

interface IAppActions {
  addToOutput(logs: string): void;
  clearOutput(): void;
  checkSchedule(checkScheduleForm: any): void;
  generateSchedule(generateScheduleForm: any): void;

  updateCourses(file: any): void;
  updatePeople(file: any): void;
  updateFaculty(file: any): void;
  resetCourses(): void;
  resetPeople(): void;
  resetFaculty(): void;
}

class AppActionsClass extends AbstractActions {
  constructor(config: AltJS.Alt) {
    super();
    this.generateActions(
      "addToOutput",
      "clearOutput",
      "checkSchedule",
      "generateSchedule",

      "updateCourses",
      "updatePeople",
      "updateFaculty",
      "resetCourses",
      "resetPeople",
      "resetFaculty",
    );
  }
}
const AppActions = alt.createActions<IAppActions>(AppActionsClass);
export { AppActions };
