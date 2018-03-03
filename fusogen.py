#coding=utf8
import itchat
import itchat.content as c
import os
import collections
import re

def validate_and_cache(fn):
    def wrapped_msg_processor(msg):
        if msg['FromUserName'] not in chatroom_names: return
        rsnd_id = []
        for r, cr in fn(msg):
            rsnd_id += [(r['MsgID'], cr)] if not r['BaseResponse']['Ret'] else []
        if rsnd_id:
            ca.update({msg['MsgId']: rsnd_id})
            ca.popitem(last=False)
    return wrapped_msg_processor

@itchat.msg_register(c.TEXT, isGroupChat=True)
@validate_and_cache
def text_relay(msg):
    for cr in chatroom_names - {msg['FromUserName']}:
        yield itchat.send_msg(u'[%s]\n%s' % (msg['ActualNickName'], msg['Content']), cr), cr

@itchat.msg_register([c.PICTURE, c.VIDEO, c.ATTACHMENT], isGroupChat=True)
@validate_and_cache
def file_relay(msg):
    if msg['Content'] == '': return # shop emoji stickers not supported
    msg.download(msg["FileName"])
    for cr in chatroom_names - {msg['FromUserName']}:
        yield itchat.send_msg('[%s]:' % msg['ActualNickName'], cr), cr
        yield itchat.send('@%s@%s' % ({'Picture': 'img', 'Video': 'vid'}.get(msg['Type'], 'fil'), msg['FileName']), cr), cr
    os.remove(msg["FileName"])

@itchat.msg_register(c.SHARING, isGroupChat=True)
@validate_and_cache
def sharing_relay(msg):
    if msg['Url'] == '': return # bundled chat history not supported
    for cr in chatroom_names - {msg['FromUserName']}:
        yield itchat.send_msg(u"[%s] 分享了链接\n%s\n%s" % (msg['ActualNickName'], msg['FileName'], msg['Url']), cr), cr

@itchat.msg_register(c.NOTE, isGroupChat=True)
def replay_revoke(msg):
    # No way to get around revoke actions rendered by itchat,
    # but it's OK 'cause msg sent by itchat is not in cache.
    if re.search(r"revokemsg", msg['Content']) is not None:
        old_msg_id = re.search("\<msgid\>(.*?)\<\/msgid\>", msg['Content']).group(1)
        for mid, un in ca.get(old_msg_id, []):
            itchat.revoke(mid, un)


itchat.auto_login(enableCmdQR=2, hotReload=True)
chatroom_names = {cr["UserName"] for cr in itchat.get_chatrooms(update=True, contactOnly=True)}
# ca's type -- {rcv_msg_id: (rsnd_msg_id, rsnd_tousername)}
ca = collections.OrderedDict([(i, []) for i in xrange(10)])
itchat.run()
