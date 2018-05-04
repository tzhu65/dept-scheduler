import * as React from "react";

export class SemesterSelect extends React.Component<null, null> {

  public render() {
    return (
      <div id="semester-select-id" className="btn-group btn-group-toggle" data-toggle="buttons">
        <label className="btn btn-secondary active">
          <input
            type="radio"
            name="semester-select"
            id="fall-semester"
            autoComplete="off"
            defaultChecked={true}
            value="fall"
          />
          Fall
        </label>
        <label className="btn btn-secondary">
          <input
            type="radio"
            name="semester-select"
            id="spring-semester"
            autoComplete="off"
            value="spring"
          />
          Spring
        </label>
      </div>
    );
  }
}
