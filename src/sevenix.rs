use base::config::keys;
use hbb_common::config;

pub const APP_NAME: &str = "SevenDesk";
const SERVER: &str = "desk.sevenix.it";
const SERVER_KEY: &str = "peHDbfz4187AzEw1LP4m1L2levY5ZigHjTn6azSqilI=";

/// `SEVENDESK_VARIANT=supporto` at build time produces the customer build,
/// which only accepts incoming connections.
pub fn is_support_build() -> bool {
    option_env!("SEVENDESK_VARIANT") == Some("supporto")
}

/// Sevenix's own server and restrictions, applied before any signed
/// `custom.txt` so the open-source rendezvous server is always used.
/// Overwrite settings cannot be changed from the UI.
pub fn apply() {
    *config::APP_NAME.write().unwrap() = APP_NAME.to_owned();
    {
        let mut overwrite = config::OVERWRITE_SETTINGS.write().unwrap();
        overwrite.insert("custom-rendezvous-server".to_owned(), SERVER.to_owned());
        overwrite.insert("relay-server".to_owned(), SERVER.to_owned());
        overwrite.insert("key".to_owned(), SERVER_KEY.to_owned());
    }
    // The open-source server has no API. Without this the client would post
    // its sysinfo (hostname, user) in plain HTTP to SERVER:21114.
    config::BUILTIN_SETTINGS
        .write()
        .unwrap()
        .insert(keys::OPTION_REGISTER_DEVICE.to_owned(), "N".to_owned());
    let mut hard = config::HARD_SETTINGS.write().unwrap();
    hard.insert("disable-account".to_owned(), "Y".to_owned());
    hard.insert("disable-ab".to_owned(), "Y".to_owned());
    if is_support_build() {
        hard.insert("conn-type".to_owned(), "incoming".to_owned());
    }
}
