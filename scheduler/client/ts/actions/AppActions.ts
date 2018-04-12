// There aren't too many actions for this app, so everything can be held here.

import { alt } from "../alt";
import { AbstractActions } from "./AbstractActions";

interface IAppActions {
  addToOutput(logs: string): void;
  clearOutput(): void;
  checkSchedule(checkScheduleForm: any): void;
  generateSchedule(generateScheduleForm: any): void;
}

class AppActionsClass extends AbstractActions {
  constructor(config: AltJS.Alt) {
    super();
    this.generateActions(
      "addToOutput",
      "clearOutput",
      "checkSchedule",
      "generateSchedule",
    );
  }
}
const AppActions = alt.createActions<IAppActions>(AppActionsClass);
export { AppActions };
