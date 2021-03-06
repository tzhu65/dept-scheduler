import * as React from "react";

export class FileUploadMode extends React.Component<null, null> {

  public render() {
    return (
      <div id="file-upload-mode-id" className="btn-group btn-group-toggle" data-toggle="buttons">
        <label className="btn btn-secondary active">
          <input
            type="radio"
            name="upload-mode"
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
            name="upload-mode"
            id="generate-schedule"
            autoComplete="off"
            value="generate"
          />
          Generate
        </label>
      </div>
    );
  }
}
