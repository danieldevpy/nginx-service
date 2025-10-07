
const BACKEND_URL = import.meta.env.VITE_BACKEND_URL;
const URL_API = `${BACKEND_URL}/settings/`

export interface ResponseError {
  statusCode: number;
  error: any;
}

export function SettingsReload(): Promise<void> {
    const urlReload = `${URL_API}reload`;
    return new Promise(async(resolve, reject) => {
        const response = await fetch(urlReload);
        if (response.ok) return resolve();
        reject();
    })
}

export function SettingsStatus(): Promise<string> {
  const urlStatus = `${URL_API}status`;
  return new Promise(async(resolve, reject) => {
    const response = await fetch(urlStatus);
    const responseJson = await response.json();
    if (response.ok) return resolve(responseJson.message as string);
    reject();
  })
}