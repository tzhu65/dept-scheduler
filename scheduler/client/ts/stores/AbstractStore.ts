class AbstractStoreModel<S> implements AltJS.StoreModel<S> {
  public bindActions: (...actions: object[]) => void;
  public bindAction: (...args: any[]) => void;
  public bindListeners: (obj: any) => void;
  public exportPublicMethods: (config: {[key: string]: (...args: any[]) => any}) => any;
  public exportAsync: (source: any) => void;
  public waitFor: any;
  public exportConfig: any;
  public getState: () => S;
  public setState: (state: any) => void;
  public emitChange: () => void;
}

export { AbstractStoreModel };
