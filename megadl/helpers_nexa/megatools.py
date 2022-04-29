# Copyright (c) 2022 Itz-fork
# Don't kang this else your dad is gae

import os
import subprocess

from config import Config

class MegaTools:
    """
    Helper class to interact with megatools cli

    Author: https://github.com/Itz-fork
    Project: https://github.com/Itz-fork/Mega.nz-Bot
    """

    def __init__(self, check_conf=True) -> None:
        self.config = "cache/config.ini"
        if check_conf:
            self.genConfig()
        else:
            print("\nConfig validation was not performed as 'check_conf=False'. Program won't work if the config was missing or corrupted!\n")
    
    def genConfig(self, sp_limit="0"):
        """
        Function to generate 'config.ini' file

        Arguments:
            sp_limit: string - Maximum speed limit for both download and upload
        """
        if os.path.isfile(self.config):
            print("\n'config.ini' file was found. Applying changes!\n")
        else:
            print("\nNo 'config.ini' file was found. Creating a new config file...\n")
        # Creating the config file
        conf_temp = f"""
[Login]
Username = {Config.MEGA_EMAIL}
Password = {Config.MEGA_PASSWORD}

[Cache]
Timeout = 10

[Network]
SpeedLimit = {sp_limit}

[Upload]
CreatePreviews = false
"""
        f = open(self.config, "w+")
        f.write(conf_temp)
        f.close()


    async def __runCommands(self, cmd):
        run = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        shell_ouput = run.stdout.read()[:-1].decode("utf-8")
        cc = await self.__checkErrors(shell_ouput)
        if cc == "retry":
            return await self.__runCommands(cmd)
        return shell_ouput
    

    async def __genErrorMsg(self, bs):
        return f"""
>>> {bs}

Please make sure that you've provided the correct username and password.

You can open a new issue if the problem persists - https://github.com/Itz-fork/Mega.nz-Bot/issues
        """


    async def __checkErrors(self, out):
        if "not found" in out:
            raise MegatoolsNotFound("'megatools' cli is not installed in this system. You can download it at - https://megatools.megous.com/")
        
        elif "Can't create directory" in out:
            raise UnableToCreateDirectory(await self.__genErrorMsg("The program wasn't able to create the directory you requested for."))
        elif "No directories specified" in out:
            raise UnableToCreateDirectory(await self.__genErrorMsg("No directory name was given."))
        
        elif "Upload failed" in out:
            raise UploadFailed(await self.__genErrorMsg("Uploading was cancelled due to an (un)known error."))
        elif "No files specified for upload" in out:
            raise UploadFailed(await self.__genErrorMsg("Path to the file which need to be uploaded wasn't provided"))

        elif "Can't login to mega.nz" in out:
            raise LoginError(await self.__genErrorMsg("Unable to login to your mega.nz account."))
        
        elif "ERROR" in out:
            raise UnknownError(await self.__genErrorMsg("Operation cancelled due to an unknown error."))
        
        else:
            return True
    

    async def download(self, link, path="MegaDownloads"):
        """
        Download file/folder from given link

        Arguments:
            link: string - Mega.nz link of the content
            path (optional): string - Path to where the content need to be downloaded
        """
        cmd = f"megadl --config {self.config} --no-progress --limit-speed 0 --path {path} {link}"
        await self.__runCommands(cmd)
        return [val for sublist in [[os.path.join(i[0], j) for j in i[2]] for i in os.walk(path)] for val in sublist]


    async def makeDir(self, path):
        """
        Make directories

        Arguments:
            path: string - Name of the directory
        """
        cmd = f"megamkdir --config {self.config} /Root/{path}"
        await self.__runCommands(cmd)


    async def upload(self, path, m_path="MegaBot"):
        """
        Upload files

        Arguments:
            path: string - Path to the file that needs to be uploaded
            m_path (optional): string - Custom path to where the files need to be uploaded
        """
        if not os.path.isfile(path):
            raise UploadFailed(await self.__genErrorMsg("Given path isn't belong to a file."))
        # Checks if the remote upload path is exists
        if not f"/Root/{m_path}" in await self.__runCommands(f"megals --config {self.config} /Root"):
            await self.makeDir(m_path)
        ucmd = f"megaput --config {self.config} --no-progress --disable-previews --no-ask-password --path /Root/{m_path} {path}"
        await self.__runCommands(ucmd)
        lcmd = f"megaexport --config {self.config} /Root/MegaBot/{os.path.basename(path)}"
        ulink = await self.__runCommands(lcmd)
        if not ulink:
            raise UploadFailed(await self.__genErrorMsg("Upload failed due to an unknown error."))
        return ulink



# Errors

class MegatoolsNotFound(Exception):
    pass

class UnableToCreateDirectory(Exception):
    pass

class UploadFailed(Exception):
    pass

class LoginError(Exception):
    pass

class UnknownError(Exception):
    pass