import * as React from "react";

export class DownloadScheduleButton extends React.Component<null, null> {
  public render() {
    return (
      <a
        id="download-schedule-btn-id"
        className="btn btn-primary disabled"
        href="#"
        role="button"
      >
        Download
      </a>
    );
  }
}
