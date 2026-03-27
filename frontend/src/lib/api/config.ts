import { env } from "$env/dynamic/public";

export const getApiBaseUrl = (): string => env.PUBLIC_API_BASE_URL || "http://localhost:8000";
