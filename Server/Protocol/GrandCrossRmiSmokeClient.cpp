#include <cstdio>
#include <chrono>

#include "ProudNetClient.h"
#include "GrandCrossRmiTypes.h"
#include "Generated/SevenDSGameC2S_proxy.h"
#include "Generated/SevenDSGameS2C_stub.h"

using namespace Proud;

namespace {
SevenDSGameC2S::Proxy g_requestProxy;
String g_responseVersion;
bool g_connected = false;
bool g_receivedVersion = false;
bool g_receivedAccount = false;
bool g_sentLogin = false;
bool g_receivedLogin = false;
NetmarbleAccountInfo g_account;

class GrandCrossS2CStub final : public SevenDSGameS2C::Stub {
public:
    DECRMI_SevenDSGameS2C_CG_RequestServerVersionOK;
    DECRMI_SevenDSGameS2C_CG_RequestAuthenticateCreateOK;
    DECRMI_SevenDSGameS2C_CG_RequestLoginOK;
};

GrandCrossS2CStub g_responseStub;
}

DEFRMI_SevenDSGameS2C_CG_RequestServerVersionOK(GrandCrossS2CStub) {
    g_responseVersion = serverVersionInfo;
    g_receivedVersion = true;
    NetmarbleSDKInfo sdk;
    sdk.storeType = _PNT("LOCAL");
    sdk.countryCode = _PNT("US");
    sdk.languageCode = _PNT("en");
    g_requestProxy.CG_RequestAuthenticateCreate(
        remote, RmiContext::ReliableSend, _PNT("smoke-local"), sdk);
    return true;
}

DEFRMI_SevenDSGameS2C_CG_RequestAuthenticateCreateOK(GrandCrossS2CStub) {
    g_account = info;
    g_receivedAccount = true;
    NetmarbleSDKInfo sdk;
    sdk.storeType = _PNT("LOCAL");
    sdk.countryCode = _PNT("US");
    sdk.languageCode = _PNT("en");
    VersionInfo version;
    version.clientVersion = 211301;
    version.cdnVersion = 0;
    const int64 loginUsn = info.usn;
    const int64 clientTick = 1;
    const int language = 0;
    const int country = 0;
    g_requestProxy.CG_RequestLogin(
        remote, RmiContext::ReliableSend, loginUsn, sdk, version,
        _PNT(""), clientTick, _PNT("local"), _PNT(""), language, country);
    g_sentLogin = true;
    return true;
}

DEFRMI_SevenDSGameS2C_CG_RequestLoginOK(GrandCrossS2CStub) {
    if (userInfo.usn == g_account.usn && !userInfo.name.IsEmpty()) {
        g_receivedLogin = true;
    }
    return true;
}

int main() {
    std::shared_ptr<CNetClient> client(CNetClient::Create());
    client->AttachProxy(&g_requestProxy);
    client->AttachStub(&g_responseStub);
    client->OnJoinServerComplete = [&](ErrorInfo* error, const ByteArray&) {
        if (!error || error->m_errorType != ErrorType_Ok) {
            std::fprintf(stderr, "ProudNet connection failed.\n");
            return;
        }
        g_connected = true;
        g_requestProxy.CG_RequestServerVersion(
            HostID_Server, RmiContext::ReliableSend);
    };

    CNetConnectionParam params;
    PNGUID protocolGuid = { 0x90cf9b2a, 0x6857, 0x4846,
        { 0xb6, 0xeb, 0x25, 0x37, 0x07, 0x76, 0x7f, 0x02 } };
    params.m_protocolVersion = Guid(protocolGuid);
    params.m_serverIP = _PNT("127.0.0.1");
    params.m_serverPort = 5001;
    params.m_closeNoPingPongTcpConnections = false;
    client->Connect(params);

    const auto deadline = std::chrono::steady_clock::now() +
        std::chrono::seconds(10);
    while (!g_receivedAccount && std::chrono::steady_clock::now() < deadline) {
        client->FrameMove();
        Proud::Sleep(10);
    }
    const auto loginDrainDeadline = std::chrono::steady_clock::now() +
        std::chrono::milliseconds(250);
    while (!g_receivedLogin && std::chrono::steady_clock::now() < loginDrainDeadline) {
        client->FrameMove();
        Proud::Sleep(10);
    }
    client->Disconnect();

    if (!g_connected || !g_receivedVersion || !g_receivedAccount || !g_receivedLogin) {
        std::fprintf(stderr, "FAIL: version/authenticate/login RMI round-trip incomplete.\n");
        return 1;
    }
    std::printf("PASS: version=%s; local account usn=%lld nickname=%s; login response decoded\n",
        StringT2A(g_responseVersion).GetString(),
        static_cast<long long>(g_account.usn),
        StringT2A(g_account.nickName).GetString());
    return 0;
}
