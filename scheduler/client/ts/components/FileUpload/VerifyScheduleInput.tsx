import * as React from "react";

import { AppActions } from "../../actions/AppActions";

import { VerifyScheduleSubmitButton } from "./VerifyScheduleSubmitButton";

export class VerifyScheduleInput extends React.Component<null, null> {

  constructor(props: any) {
    super(props);
    this.onSubmit = this.onSubmit.bind(this);
  }

  public onSubmit(e: any) {
    e.preventDefault();
    const verifyScheduleForm = new FormData(($("#verify-schedule-id")[0] as HTMLFormElement));
    AppActions.checkSchedule(verifyScheduleForm);
  }

  public render() {
    return (
      <div>
        <form
          id="verify-schedule-id"
          action="/verifySchedule"
          method="post"
          encType="multipart/form-data"
          onSubmit={this.onSubmit}
        >
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

          <VerifyScheduleSubmitButton />

        </form>
      </div>
    );
  }
}
