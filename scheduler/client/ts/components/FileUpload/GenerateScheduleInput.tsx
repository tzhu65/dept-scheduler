import * as React from "react";

import { AppActions } from "../../actions/AppActions";

import { GenerateScheduleSubmitButton } from "./GenerateScheduleSubmitButton";

export class GenerateScheduleInput extends React.Component<null, null> {

  constructor(props: any) {
    super(props);
    this.onSubmit = this.onSubmit.bind(this);
  }

  public onSubmit(e: any) {
    e.preventDefault();
    const generateScheduleForm = new FormData(($("#generate-schedule-id")[0] as HTMLFormElement));
    AppActions.generateSchedule(generateScheduleForm);
  }

  public render() {
    return (
      <div>
        <form
          id="generate-schedule-id"
          action="/generateSchedule"
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

          <GenerateScheduleSubmitButton />

        </form>
      </div>
    );
  }
}
