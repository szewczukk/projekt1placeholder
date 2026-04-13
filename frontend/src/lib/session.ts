import { browser } from "$app/environment";
import { getApiBaseUrl } from "$lib/api/config";

const STORAGE_KEY = "shop_user_id";
const SESSION_QUERY_PARAM = "sessionId";

let sessionPromise: Promise<void> | null = null;

function randomUserId(): number {
	const max = 2 ** 31 - 1;
	return 1 + Math.floor(Math.random() * max);
}

function parsePositiveInt(value: string | null): number | null {
	if (!value) {
		return null;
	}
	const n = Number.parseInt(value, 10);
	if (Number.isNaN(n) || n <= 0) {
		return null;
	}
	return n;
}

export function ensureSessionIdInUrl(): number {
	if (!browser) {
		return 0;
	}
	const currentUrl = new URL(window.location.href);
	const fromQuery = parsePositiveInt(currentUrl.searchParams.get(SESSION_QUERY_PARAM));
	if (fromQuery) {
		localStorage.setItem(STORAGE_KEY, String(fromQuery));
		return fromQuery;
	}

	const fromStorage = parsePositiveInt(localStorage.getItem(STORAGE_KEY));
	const sessionId = fromStorage ?? randomUserId();
	currentUrl.searchParams.set(SESSION_QUERY_PARAM, String(sessionId));
	window.history.replaceState(window.history.state, "", currentUrl);
	localStorage.setItem(STORAGE_KEY, String(sessionId));
	return sessionId;
}

export function getUserId(): number {
	if (!browser) {
		return 0;
	}
	return ensureSessionIdInUrl();
}

export function ensureSession(fetchFn: typeof fetch = fetch): Promise<void> {
	if (!browser) {
		return Promise.resolve();
	}
	if (!sessionPromise) {
		const userId = getUserId();
		sessionPromise = fetchFn(`${getApiBaseUrl()}/sessions`, {
			method: "POST",
			headers: { "Content-Type": "application/json" },
			body: JSON.stringify({ user_id: userId }),
		})
			.then((res) => {
				if (!res.ok) {
					sessionPromise = null;
					throw new Error(`Sesja nie została utworzona (${res.status})`);
				}
			})
			.catch((err) => {
				sessionPromise = null;
				throw err;
			});
	}
	return sessionPromise;
}
