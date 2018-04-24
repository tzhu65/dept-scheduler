import * as React from "react";

import { AppActions } from "../../actions/AppActions";

import { DownloadScheduleButton } from "./DownloadScheduleButton";
import { FileInputSubmitButton } from "./FileInputSubmitButton";
import { FileUploadMode } from "./FileUploadMode";

export class FileInputForm extends React.Component<null, null> {

  public onSubmit(e: any) {
    e.preventDefault();
    const fileInputForm = new FormData(($("#file-input-id")[0] as HTMLFormElement));
    const mode = $("#file-input-id input:radio:checked").val();
    if (mode === "check") {
      AppActions.checkSchedule(fileInputForm);
    } else if (mode === "generate") {
      AppActions.generateSchedule(fileInputForm);
    }
  }

  public render() {
    return (
      <div>
        <form
          id="file-input-id"
          action="/verifySchedule"
          method="post"
          encType="multipart/form-data"
          onSubmit={this.onSubmit}
        >
          <FileUploadMode />

          <div className="form-group">
            <label htmlFor="vs-courses-input-id"><b>Schedule</b></label>
            <input id="vs-courses-input-id" className="form-control-file" type="file" name="courses" required={true}/>
          </div>

          <div className="form-group">
            <label htmlFor="vs-people-input-id"><b>TA Preferences</b></label>
            <input id="vs-people-input-id" className="form-control-file" type="file" name="people" required={true}/>
          </div>

          <div className="form-group">
            <label htmlFor="vs-faculty-input-id"><b>Faculty Hours</b></label>
            <input id="vs-faculty-input-id" className="form-control-file" type="file" name="faculty" required={true}/>
          </div>

          <FileInputSubmitButton />
          <DownloadScheduleButton />

        </form>
      </div>
    );
  }
}
