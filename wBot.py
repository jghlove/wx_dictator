# -*- coding: utf-8 -*-
from wxpy import *
from aip import AipSpeech
import config as config
import os
#import requests
#import random
import re
import time
#import codecs

class WBot(object):
    def __init__(self):
#        self.bot = Bot(True, 2)
        self.bot = Bot()
        self.bot.enable_puid()
        self.bot.messages.max_history = config.MAX_HISTORY
        #self.tuling = Tuling(api_key=config.TULING_API_KEY)
        self.aipSpeech = AipSpeech(
            config.BAIDU_VOICE[u'app_id'],
            config.BAIDU_VOICE[u'api_key'],
            config.BAIDU_VOICE[u'secret_key']
        )
        #self.session = requests.Session()
        #self.tulingUrl = config.TULING_URL
        #self.input=self.bot.groups().search(config.INPUT_CHAT_NAME)[0]
        #self.output=self.bot.friends().search(config.OUTPUT_CHAT_NAME)[0]

    def run(self):
        #self.auto_reply_tuling_robot()
        #self.auto_accept_friends()
        #self.recalled_message_helper()
        self.bot.file_helper.send(u'机器人建立:')
        # self.output.send(u'机器人建立:')
        # self.input.send(u'讲座开始：')
        # self.auto_weidian()
        self.auto_daka()
        self.voice_message_helper()
        embed()

    ### Message Listener ###
    '''
    def auto_reply_tuling_robot(self):
        """
        注册图灵机器人聊天对象
        单聊回复
        群聊@回复
        
        Message Type: TEXT
        :return: 
        """
        @self.bot.register(chats=self.wxl,msg_types=TEXT)
        def auto_reply(msg):
            if isinstance(msg.chat, Group) and not msg.is_at:
                return
            else:
                ret = self.tuling.reply_text(msg, True)
                ret = ret.replace(u'图灵机器人', self.bot.self.nick_name)
                msg.reply(ret)



    def recalled_message_helper(self):
        """
        对撤回的消息进行处理
        
        Message Type: NOTE
        :return: 
        """
        @self.bot.register(chats=self.wxl,msg_types=NOTE)
        def auto_display(msg):
            msg_content = msg.raw.get('Content')
            if re.search(u'<!\[CDATA\[.*撤回了一条消息\]\]>', msg_content) is not None:
                recalled_msg_id = re.search(u'<msgid>(.*?)</msgid>', msg_content).group(1)
                recalled_msg = self._search_message_by_id(recalled_msg_id)
                if recalled_msg.type == TEXT:
                    if isinstance(msg.chat, Friend):
                        text_msg = recalled_msg.sender.nick_name + \
                                   u' 撤回了一条消息：' + self._message_truncation(recalled_msg.text)
                    elif isinstance(msg.chat, Group):
                        text_msg = recalled_msg.raw.get('ActualNickName') + \
                                   u' 撤回了一条消息：' + self._message_truncation(recalled_msg.text)
                    else:
                        text_msg = recalled_msg.sender.nick_name + u' 撤回了一条消息'
                    msg.reply(text_msg)

    '''
    def auto_weidian(self):     
        @self.bot.register(msg_types=TEXT,except_self=False)
        def auto_reply_weidian(msg):
            sender_name = msg.sender.name
            whtx = u'文话童心'
            if isinstance(msg.chat, Group):
                pass
            else:
                return
            if sender_name.find(whtx) < 0:
                return
            else:
                pass
                #self.bot.file_helper.send('Someone talking about '+ whtx)
            if msg.text == u'微店':
                weidian_address=u'https://weidian.com/s/161180129?src=shop&wfr=wx&from=groupmessage'
                msg.reply(weidian_address)
            elif msg.text.find(u'小帅舅舅') >= 0:
                msg.reply(u'在！')
            else:
                return

    def auto_daka(self):    # 自动整理打卡
        @self.bot.register(msg_types=TEXT,except_self=False)
        def auto_reply_weidian(msg):
            sender_name = msg.sender.name
            whtx = u'坚持阅读拒绝碎片'
            if isinstance(msg.chat, Group): # 判断是不是群聊
                pass
            else:
                return
            if sender_name.find(whtx) < 0:  # 判断群聊名称
                return
            else:
                pass
            if msg.text.find(u'读书打卡') < 0:
                return
            else:
                notes = msg.text
                u_name = msg.member.name
                try:
                    output_file_object = open('notes.txt','a')
                except:
                    self.bot.file_helper.send(u'输出文件打开失败')
                else:
                    pass
                try:
                    output_file_object.write(u_name.encode('gb18030','ignore'))
                    output_file_object.write('\t')
                    output_file_object.write(notes.encode('gb18030','ignore'))
                    output_file_object.write('\n')
                except:
                    self.bot.file_helper.send(u'文件写入失败')
                finally:
                    output_file_object.close()



    ### Multimedia Message Process ###
    def voice_message_helper(self):
        """
        对语音消息进行处理
        
        :return: 
        """
        @self.bot.register(msg_types=RECORDING,except_self=False)
        def auto_process(msg):
            day = time.strftime('%Y-%m-%d',time.localtime(time.time()))  #get current time
            sender_name = msg.sender.name
            output_folder = os.getcwd()+u'\\' + u'Voices\\' + sender_name
            if not os.path.exists(output_folder):
                    try:
                        os.makedirs(output_folder)
                    except:
                        self.bot.file_helper.send('fail to make output folder for ' + sender_name)
                        return
                    else:
                        pass
            output_path = output_folder+u'\\'+ day +u'.txt'
            # bot.file_helper.send(u'文件输出地址：'+self.output_path)
            try:
                output_file_object = open(output_path,'a')
            except:
                self.bot.file_helper.send(u'输出文件打开失败')
            else:
                pass
            
            file_path = self._download_attachment(msg, RECORDING)
            if file_path:
                audio_path = self._audio_conversion(file_path)
                if os.path.isfile(audio_path):
                    response = self.aipSpeech.asr(self._get_file_content(audio_path), 'wav', 8000, {
                        'lan': 'zh',
                    })
                    #res_msg = self._next_topic()
                    if response[u'err_no'] == 0:
                        text = response[u'result'][0]
                            #user_id = re.sub(r'[^a-zA-Z\d]', '', msg.sender.user_name)
                            #answer = self._tuling_msg(message=text, user_id=user_id)
                            #res_msg = self._process_answer(answer)
                        # self.output.send(text)
                        if isinstance(msg.chat, Group):
                            text = msg.member.name + u':' + text
                        else:
                            pass
                        #self.bot.file_helper.send(type(text))
                        try:
                            output_file_object.write(text.encode('gb18030','ignore'))
                            output_file_object.write('\n')
                        except:
                            self.bot.file_helper.send(u'文件写入失败')
                        finally:
                            output_file_object.close()
                        if config.COPY_TO_FILE_HELPER == True:
                            self.bot.file_helper.send(text)

    ### Helper Function ###
    def _search_message_by_id(self, message_id):
        """
        从缓存历史消息中根据消息ID查询消息
        
        :return: 
        """
        for msg in self.bot.messages:
            if message_id == str(msg.id):
                return msg
        return None

    @staticmethod
    def _message_truncation(msg):
        """
        消息长度截取，避免消息过长 产生炸群嫌疑
        
        :param msg: 
        :return: 
        """
        if msg and len(msg) > config.MESSAGE_LENGTH:
            msg = msg[0:config.MESSAGE_LENGTH] + u'...'
        return msg

    def _download_attachment(self, msg, msg_type):
        """
        下载文件到对应文件夹
        
        :param msg: 
        :param msg_type: 
        :return: 
        """
        file_path = self._get_storage_path(msg, msg_type)
        msg.get_file(save_path=file_path)
        if os.path.isfile(file_path) and os.path.getsize(file_path) > 0:
            return file_path
        else:
            # self.output.send('os.path.isfile(file_path) and os.path.getsize(file_path) < 0')
            return None

    @staticmethod
    def _get_storage_path(msg, msg_type):
        """
        Get File Path
        
        :param msg: 
        :param msg_type: 
        :return: 
        """
        puid = msg.sender.puid if msg.sender.puid else u'other'
        path = config.STORAGE_PATH + msg_type.lower() + u'/' + puid
        absolute_path = os.getcwd()
        if path:
            path_list = path.split(u'/')
            for folder in path_list:
                absolute_path = absolute_path + u'/' + folder
                if not os.path.exists(absolute_path):
                    os.makedirs(absolute_path)
                    f=open(absolute_path+u'/name.txt','a')
                    f.write(msg.sender.name.encode('gb18030','ignore'))
                    f.close()
            absolute_path = absolute_path + u'/' + msg.file_name
        return absolute_path

    @staticmethod
    def _audio_conversion(path, audio_format='.wav', sample_rate='8000'):
        """
        Audio Conversion
        
        :param path: 
        :return: 
        """
        filename, file_extension = os.path.splitext(path)
        audio_path = filename + audio_format
        path = path.decode('utf8').encode('GBK')
        conversion_command = u'ffmpeg -i ' + path + u' -acodec pcm_s16le -ar ' + sample_rate + u' ' + audio_path
        os.system(conversion_command)

        return audio_path

    @staticmethod
    def _get_file_content(file_path):
        with open(file_path, 'rb') as fp:
            return fp.read()
            
'''
    ### Tuling Function ###
    def _tuling_msg(self, message, user_id):
        """
        向Tuling发送消息
        :param message: 
        :param user_id: 
        :return: 
        """
        payload = dict(
            key=config.TULING_API_KEY,
            info=message,
            userid=user_id,
            loc=None
        )
        # noinspection PyBroadException
        try:
            r = self.session.post(self.tulingUrl, json=payload)
            answer = r.json()
        except:
            answer = None

        return answer

    def _process_answer(self, answer):
        """
        解析Tuling返回消息
        
        :param answer: 
        :return: 
        """
        ret = self._next_topic()
        code = -1
        if answer:
            code = answer.get('code', -1)

        if code >= 100000:
            text = answer.get('text')
            if text:
                ret = text
        return ret

    @staticmethod
    def _next_topic():
        """
        聊天机器人无法获取回复时的备用回复
        """

        return random.choice((
            u'小主人，我听不清楚呢！',
            u'你再说一遍嘛'
        ))
'''