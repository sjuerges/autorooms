from .autorooms import AutoRooms


def setup(bot):
    bot.add_cog(AutoRooms(bot))
