from discord.ext import commands
from discord.ext.commands import Context

import mary.mctourdb.mctourdb as db
import mary.mctourdb.model.project as project
from mary.mctourdb.model import review


def setup(bot):
    bot.add_cog(McTour(bot))

def listPrint(list):
    out = ''
    for l in list:
        out = out + str(l) + '\n'
    return out


class McTour(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = db.create_connection("McTour.db")
        db.create_table(self.db,project.sql_create_projects_table)
        db.create_table(self.db,review.sql_create_reviews_table)


    @commands.command()
    async def mctour(self,ctx:Context):
        await ctx.send('Track and review various Minecraft project with my commands in this category, or use my knowledge to get a guided tour of the SSAGO minecraft server!')


    @commands.command()
    async def project(self,ctx:Context,name:str,warp:str, map_url:str, *, description:str):
        """
        add or update a project
        :param name name of the project
        :param nearest warp for the project
        :param map_url url for viewing the project on the map
        :param description of the project, multiple words allowed.
        """
        p = project.Project(name,warp,map_url,description)
        await ctx.send('{0}: {1}'.format(p.save_project(self.db),name))

    @commands.command()
    async def review(self,ctx:Context,project_id:str,rating:int,*,description:str):
        """
        add or update a review
        :param project_id: id of the project to review
        :param rating: rating out of 10 for the project
        :param description: description of the review
        """
        r = review.Review(None,ctx.author.name,project_id,rating,description)
        await ctx.send('{0} by {1} about {2}'.format(r.save_review(self.db),ctx.author.name,project_id))

    @commands.command()
    async def view(self,ctx:Context,name:str):
        """
        view a project
        :param name the projects name
        """
        ps = project.select_project_by_name(self.db, name)
        if ps is None:
            await ctx.send('No Project by this name')
        else:
            reviews = review.select_reviews_by_project(self.db,name)
            await ctx.send("{0}\n {1}".format(ps,listPrint(reviews)))

    @commands.command()
    async def projects(self,ctx:Context):
        """views all the projects"""
        ps = project.select_all_projects(self.db)
        if ps is None or len(ps) == 0:
            await ctx.send('No Projects available')
        else:
            await ctx.send(listPrint(ps))

    @commands.command()
    async def next(self,ctx:Context):
        """Picks a random project for you to visit"""
        ps = project.get_random_project(self.db)
        if ps is None:
            await ctx.send('No Projects available')
        else:
            reviews = review.select_reviews_by_project(self.db, ps.name)
            await ctx.send("{0}\n {1}".format(ps, listPrint(reviews)))

