import { browser } from "$app/environment";
import { getApiBaseUrl } from "$lib/api/config";

const STORAGE_KEY = "shop_user_id";

let sessionPromise: Promise<void> | null = null;

function randomUserId(): number {
	const max = 2 ** 31 - 1;
	return 1 + Math.floor(Math.random() * max);
}

export function getUserId(): number {
	if (!browser) {
		return 0;
	}
	const raw = localStorage.getItem(STORAGE_KEY);
	if (raw) {
		const n = Number.parseInt(raw, 10);
		if (!Number.isNaN(n) && n > 0) {
			return n;
		}
	}
	const id = randomUserId();
	localStorage.setItem(STORAGE_KEY, String(id));
	return id;
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
