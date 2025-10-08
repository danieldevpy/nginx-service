const CUSTOM_URL = import.meta.env.VITE_API_URL;
const API_URL = CUSTOM_URL? `${CUSTOM_URL}/settings/` : '/settings/';

console.log(API_URL)

export interface ResponseError {
  statusCode: number;
  error: any;
}

export function SettingsReload(): Promise<void> {
    const urlReload = `${API_URL}reload`;
    return new Promise(async(resolve, reject) => {
        const response = await fetch(urlReload);
        if (response.ok) return resolve();
        reject();
    })
}

export function SettingsStatus(): Promise<string> {
  const urlStatus = `${API_URL}status`;
  return new Promise(async(resolve, reject) => {
    const response = await fetch(urlStatus);
    const responseJson = await response.json();
    if (response.ok) return resolve(responseJson.message as string);
    reject();
  })
}