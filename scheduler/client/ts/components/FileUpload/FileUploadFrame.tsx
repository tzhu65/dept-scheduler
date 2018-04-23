import * as React from "react";

import { DownloadScheduleButton } from "./DownloadScheduleButton";
import { GenerateScheduleInput } from "./GenerateScheduleInput";
import { VerifyScheduleInput } from "./VerifyScheduleInput";

export class FileUploadFrame extends React.Component<null, null> {
  public render() {
    return (
      <div>

        <nav className="navbar navbar-expand-lg">
          <ul className="nav nav-pills" id="mode-tabs" role="mode-selection">
            <li className="nav-item">
              <a
                className="nav-link active"
                id="check-tab"
                data-toggle="tab"
                href="#check"
                role="tab"
                aria-controls="check"
                aria-selected="true"
              >
                Check
              </a>
            </li>
            <li className="nav-item">
              <a
                className="nav-link"
                id="generate-tab"
                data-toggle="tab"
                href="#generate"
                role="tab"
                aria-controls="generate"
                aria-selected="false"
              >
                Generate
              </a>
            </li>
          </ul>
        </nav>

        <div className="tab-content">
          <div className="tab-pane fade show active" id="check" role="tabpanel" aria-labelledby="check-tab">
            <VerifyScheduleInput />
          </div>
          <div className="tab-pane fade" id="generate" role="tabpanel" aria-labelledby="generate-tab">
            <GenerateScheduleInput />
            <DownloadScheduleButton />
          </div>
        </div>

      </div>
    );
  }
}
