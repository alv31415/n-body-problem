export function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

export const LOCAL_BASE_URL = "127.0.0.1:8000";
export const DEPLOY_URL = "https://nbody-api.herokuapp.com/api/";

export const GET_NBODY_IDS_URL = DEPLOY_URL + "nbody-list-ids/";
export const GET_INTEGRATOR_IDS_URL = DEPLOY_URL + "integrator-list-ids/";
export const POST_INTEGRATOR_UPDATE_URL = DEPLOY_URL + "integrator-update/";
export const POST_NBODY_CREATE_URL = DEPLOY_URL + "nbody-create/";
export const POST_INTEGRATOR_CREATE_URL = DEPLOY_URL + "integrator-create/";
