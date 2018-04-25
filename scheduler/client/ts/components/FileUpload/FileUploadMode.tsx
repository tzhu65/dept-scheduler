import * as React from "react";

export class FileUploadMode extends React.Component<null, null> {

  public render() {
    return (
      <div className="row">
        <div className="justify-content-center">
          <div className="btn-group btn-group-toggle" data-toggle="buttons">
            <label className="btn btn-secondary active">
              <input
                type="radio"
                name="options"
                id="check-schedule"
                autoComplete="off"
                defaultChecked={true}
                value="check"
              />
              Check
            </label>
            <label className="btn btn-secondary">
              <input
                type="radio"
                name="options"
                id="generate-schedule"
                autoComplete="off"
                value="generate"
              />
              Generate
            </label>
          </div>
        </div>
      </div>
    );
  }
}
