import { alt } from "../alt";

import { AbstractStoreModel } from "./AbstractStore";

import { AppActions } from "../actions/AppActions";

interface IAPICallerStoreState {
  loading: boolean;
  delay: string;
}
export { IAPICallerStoreState };

class APICallerStoreClass extends AbstractStoreModel<IAPICallerStoreState> implements IAPICallerStoreState {
  public loading: boolean;
  public delay: string;

  constructor() {
    super();
    this.loading = false;
    this.delay = "";
    this.bindAction(AppActions.checkSchedule, this.onCheckSchedule);
    this.bindAction(AppActions.generateSchedule, this.onGenerateSchedule);
  }

  public onCheckSchedule() {
    if (this.loading) {
      return;
    }
    this.loading = true;
    this.delay = "";
    const start = new Date().getTime();
    $.ajax({
      url: "verifySchedule",
      type: "POST",
      data: new FormData(($("#verify-schedule-id")[0] as HTMLFormElement)),
      cache: false,
      contentType: false,
      processData: false,

      // Custom XMLHttpRequest
      xhr: () => {
        const myXhr = $.ajaxSettings.xhr();
        if (myXhr.upload) {
          // For handling the progress of the upload
          myXhr.upload.addEventListener("progress", (event: any) => {
            if (event.lengthComputable) {
              console.log(event.loaded, event.total);
            }
          }, false);
        }
        return myXhr;
      },

      success: (data: any, status: string, xhr: JQuery.jqXHR) => {
        AppActions.addToOutput("Finished checking the schedule...");
        data.errors.map((e: string) => {
          AppActions.addToOutput(e);
        });
        const time = new Date().getTime() - start;
        this.setState({loading: false, delay: time.toString() + "ms"});
      },
      error: (xhr: JQuery.jqXHR, status: string, error: string) => {
        AppActions.addToOutput(`ERROR\t${status}\t${JSON.stringify(error, null, 2)}`);
        const time = new Date().getTime() - start;
        this.setState({loading: false, delay: time.toString() + "ms"});
      },
    });
  }

  public onGenerateSchedule(generateScheduleForm: any) {
    if (this.loading) {
      return;
    }
    this.loading = true;
    this.delay = "";
    const start = new Date().getTime();
    $.ajax({
      url: "generateSchedule",
      type: "POST",
      data: generateScheduleForm,
      cache: false,
      contentType: false,
      processData: false,

      // Custom XMLHttpRequest
      xhr: () => {
        const myXhr = $.ajaxSettings.xhr();
        if (myXhr.upload) {
          // For handling the progress of the upload
          myXhr.upload.addEventListener("progress", (event: any) => {
            if (event.lengthComputable) {
              console.log(event.loaded, event.total);
            }
          }, false);
        }
        return myXhr;
      },

      success: (data: any, status: string, xhr: JQuery.jqXHR) => {
        AppActions.addToOutput(`JSON data response: ${JSON.stringify(data, null, 2)}`);
        const time = new Date().getTime() - start;
        this.setState({loading: false, delay: time + "ms"});
      },
      error: (xhr: JQuery.jqXHR, status: string, error: string) => {
        AppActions.addToOutput(`ERROR\t${status}\t${error}`);
        const time = new Date().getTime() - start;
        this.setState({loading: false, delay: time + "ms"});
      },
    });
  }
}
const APICallerStore = (alt as any).createStore(APICallerStoreClass, "APICallerStore");
export { APICallerStore };
