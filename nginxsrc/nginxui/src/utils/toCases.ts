

export function ToCamelCase(obj: any): any {
  if (Array.isArray(obj)) {
    return obj.map(ToCamelCase);
  } else if (obj !== null && typeof obj === "object") {
    return Object.keys(obj).reduce((acc, key) => {
      const camelKey = key.replace(/_([a-z])/g, (_, letter) => letter.toUpperCase());
      acc[camelKey] = ToCamelCase(obj[key]);
      return acc;
    }, {} as any);
  }
  return obj;
}

export function ToSnakeCase(obj: any): any {
  if (Array.isArray(obj)) {
    return obj.map(ToSnakeCase);
  } else if (obj !== null && typeof obj === "object") {
    return Object.keys(obj).reduce((acc, key) => {
      const snakeKey = key.replace(/([A-Z])/g, "_$1").toLowerCase();
      acc[snakeKey] = ToSnakeCase(obj[key]);
      return acc;
    }, {} as any);
  }
  return obj;
}
