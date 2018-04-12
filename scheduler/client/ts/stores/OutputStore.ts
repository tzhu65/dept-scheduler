import { alt } from "../alt";

import { AbstractStoreModel } from "./AbstractStore";

import { AppActions } from "../actions/AppActions";

interface IOutputStoreState {
  logs: string[];
}
export { IOutputStoreState };

class OutputStoreClass extends AbstractStoreModel<IOutputStoreState> implements IOutputStoreState {
  public logs: string[];

  constructor() {
    super();
    this.logs = [];
    this.bindAction(AppActions.addToOutput, this.onAddToOutput);
    this.bindAction(AppActions.clearOutput, this.onClearOutput);
  }

  public onAddToOutput(log: string) {
    this.logs.push(log);
  }

  public onClearOutput() {
    this.logs = [];
  }
}
const OutputStore = (alt as any).createStore(OutputStoreClass, "OutputStore");
export { OutputStore };
