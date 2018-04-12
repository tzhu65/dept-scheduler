import * as React from "react";

import { Navbar } from "./Navbar/Navbar";
import { FileUploadFooter } from "./FileUpload/FileUploadFooter";
import { FileUploadFrame } from "./FileUpload/FileUploadFrame";
import { OutputFrame } from "./Output/OutputFrame";
import { AboutInfo } from "./Modals/AboutInfo";

export class Frame extends React.Component<null, null> {
  public render() {
    return (
      <div className="container-fluid">
        <div className="row fill-screen">

          <div className="col-sm-4 file-upload-frame">
            <FileUploadFrame />
            <FileUploadFooter />
          </div>

          <div className="col-sm-8 output-frame">
            <OutputFrame />
          </div>

        </div>

        <AboutInfo />
        <Navbar />

      </div>
    );
  }
}
