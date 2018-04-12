class AbstractActions implements AltJS.ActionsClass {
  public actions: any;
  public dispatch: (...payload: any[]) => void;
  public generateActions: (...actions: string[]) => void;
}

export { AbstractActions };
