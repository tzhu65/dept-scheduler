import { alt } from "../alt";

import { AbstractStoreModel } from "./AbstractStore";

import { AppActions } from "../actions/AppActions";

interface IFileUploadFormStoreState {
  coursesLastUploaded: string;
  coursesFileName: string;

  peopleLastUploaded: string;
  peopleFileName: string;

  facultyLastUploaded: string;
  facultyFileName: string;
}
export { IFileUploadFormStoreState };

class FileUploadFormStoreClass extends AbstractStoreModel<IFileUploadFormStoreState>
  implements IFileUploadFormStoreState {

  public coursesLastUploaded: string;
  public coursesFileName: string;
  public coursesFile: string;

  public peopleLastUploaded: string;
  public peopleFileName: string;
  public peopleFile: string;

  public facultyLastUploaded: string;
  public facultyFileName: string;
  public facultyFile: string;

  public keys: {[keyName: string]: {fileName: string, file: string, lastUploaded: string}} = {
    courses: {
      fileName: "courses-filename",
      file: "courses",
      lastUploaded: "courses-last-uploaded",
    },
    people: {
      fileName: "people-filename",
      file: "people",
      lastUploaded: "people-last-uploaded",
    },
    faculty: {
      fileName: "faculty-filename",
      file: "faculty",
      lastUploaded: "faculty-last-uploaded",
    },
  };

  constructor() {
    super();

    // Get the times each spreadsheet was last Uploaded
    this.coursesLastUploaded = window.localStorage.getItem(this.keys.courses.lastUploaded);
    this.peopleLastUploaded = window.localStorage.getItem(this.keys.people.lastUploaded);
    this.facultyLastUploaded = window.localStorage.getItem(this.keys.faculty.lastUploaded);

    this.coursesFileName = window.localStorage.getItem(this.keys.courses.fileName);
    this.peopleFileName = window.localStorage.getItem(this.keys.people.fileName);
    this.facultyFileName = window.localStorage.getItem(this.keys.faculty.fileName);

    this.bindAction(AppActions.updateCourses, this.onUpdateCourses);
    this.bindAction(AppActions.updatePeople, this.onUpdatePeople);
    this.bindAction(AppActions.updateFaculty, this.onUpdateFaculty);
    this.bindAction(AppActions.resetCourses, this.onResetCourses);
    this.bindAction(AppActions.resetPeople, this.onResetPeople);
    this.bindAction(AppActions.resetFaculty, this.onResetFaculty);

    this.exportPublicMethods({
      getCoursesFile: this.getCoursesFile.bind(this),
      getPeopleFile: this.getPeopleFile.bind(this),
      getFacultyFile: this.getFacultyFile.bind(this),
    });
  }

  public getCoursesFile() {
    return window.localStorage.getItem(this.keys.courses.file);
  }

  public getPeopleFile() {
    return window.localStorage.getItem(this.keys.people.file);
  }

  public getFacultyFile() {
    return window.localStorage.getItem(this.keys.faculty.file);
  }

  public onUpdateCourses(file: any) {
    return this.readerHelper(file, (fileName: string, text: string) => {
      this.coursesFileName = fileName;
      window.localStorage.setItem(this.keys.courses.fileName, fileName);
      window.localStorage.setItem(this.keys.courses.file, text);

      this.coursesLastUploaded = new Date().getTime().toString();
      window.localStorage.setItem(this.keys.courses.lastUploaded, this.coursesLastUploaded);
      this.emitChange();
    });
  }

  public onUpdatePeople(file: any) {
    return this.readerHelper(file, (fileName: string, text: string) => {
      this.peopleFileName = fileName;
      window.localStorage.setItem(this.keys.people.fileName, fileName);
      window.localStorage.setItem(this.keys.people.file, text);

      this.peopleLastUploaded = new Date().getTime().toString();
      window.localStorage.setItem(this.keys.people.lastUploaded, this.peopleLastUploaded);
      this.emitChange();
    });
  }

  public onUpdateFaculty(file: any) {
    return this.readerHelper(file, (fileName: string, text: string) => {
      this.facultyFileName = fileName;
      window.localStorage.setItem(this.keys.faculty.fileName, fileName);
      window.localStorage.setItem(this.keys.faculty.file, text);

      this.facultyLastUploaded = new Date().getTime().toString();
      window.localStorage.setItem(this.keys.faculty.lastUploaded, this.facultyLastUploaded);
      this.emitChange();
    });
  }

  public onResetCourses() {
    this.coursesLastUploaded = null;
    this.coursesFileName = null;
    window.localStorage.removeItem(this.keys.courses.lastUploaded);
    window.localStorage.removeItem(this.keys.courses.fileName);
    window.localStorage.removeItem(this.keys.courses.file);
  }

  public onResetPeople() {
    this.peopleLastUploaded = null;
    this.peopleFileName = null;
    window.localStorage.removeItem(this.keys.people.lastUploaded);
    window.localStorage.removeItem(this.keys.people.fileName);
    window.localStorage.removeItem(this.keys.people.file);
  }

  public onResetFaculty() {
    this.facultyLastUploaded = null;
    this.facultyFileName = null;
    window.localStorage.removeItem(this.keys.faculty.lastUploaded);
    window.localStorage.removeItem(this.keys.faculty.fileName);
    window.localStorage.removeItem(this.keys.faculty.file);
  }

  private readerHelper(file: any, cb: any) {
    const reader = new FileReader();
    reader.onload = (event: any) => {
      return cb(file.name, event.target.result);
    };
    return reader.readAsText(file);
  }

}
const FileUploadFormStore = (alt as any).createStore(FileUploadFormStoreClass, "FileUploadFormStore");
export { FileUploadFormStore };
